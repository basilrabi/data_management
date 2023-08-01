#!/usr/bin/Rscript

source("scripts/R/pull_manila_gps_common.R")

library(stringr)

latest_status <- RPostgres::dbGetQuery(con, "
select equipment_id as id, max(time_stamp) as max_status
from fleet_equipmentignitionstatus
group by equipment_id
                                      ") %>%
  dplyr::mutate(max_status = lubridate::with_tz(max_status, "Asia/Manila"))

equipment_list <- dplyr::left_join(dm_equipment, latest_status) %>%
  dplyr::left_join(latest_point) %>%
  dplyr::mutate(start = dplyr::case_when(
    !is.na(max_status) ~ max_status + lubridate::seconds(1),
    TRUE ~ as.POSIXct(minimum_timestamp)
  )) %>%
  dplyr::filter(start < max)

if (any(is.na(equipment_list$id))) {
  stop("Unregistered equipment detected.")
}

ignition_period <- lapply(1:nrow(equipment_list), function(x) {
  data.frame(
    tracker_id = equipment_list$tracker_id[x],
    start = seq(from = equipment_list$start[x],
                to = equipment_list$max[x],
                by = "7 days")
  )
}) %>%
  dplyr::bind_rows() %>%
  dplyr::left_join(dplyr::select(equipment_list, tracker_id, max)) %>%
  dplyr::mutate(next_week = start + lubridate::days(7) - lubridate::seconds()) %>%
  dplyr::mutate(end = dplyr::case_when(next_week > max ~ max, TRUE ~ next_week))


lapply(1:nrow(ignition_period), function(z) {
  url <- paste0(
    host,
    "history/tracker/list/?trackers=[",
    ignition_period$tracker_id[z],
    "]&from=",
    format(ignition_period$start[z], format = "%Y-%m-%d%%20%H:%M:%S"),
    "&to=",
    format(ignition_period$end[z], format = "%Y-%m-%d%%20%H:%M:%S"),
    "&",
    hash
  )
  api_output <- pull_retry(url)
  cat(sprintf("Processing %s out of %s.\n", z, nrow(ignition_period)))
  if (is.data.frame(api_output)) {
    equipment_id <- equipment_list$id[equipment_list$tracker_id == ignition_period$tracker_id[z]]
    output <- dplyr::filter(api_output,
                            stringr::str_detect(message, "Ignition")) %>%
      dplyr::arrange(time)
    if (nrow(output) > 0) {
      cat(url, "\n")
      df_ignition <- lapply(1:nrow(output), function(i) {
        data.frame(equipment_id = equipment_id,
                   time_stamp = output$time[i],
                   ignition = stringr::str_detect(output$message[i], "ON$"))
      }) %>%
        dplyr::bind_rows() %>%
        dplyr::group_by(equipment_id, time_stamp, ignition) %>%
        dplyr::summarise() %>%
        dplyr::group_by(time_stamp) %>%
        dplyr::mutate(n = dplyr::n()) %>%
        dplyr::filter(n < 2)
      table_name <- paste0(ignition_period$tracker_id[z],
                           "-",
                           as.Date(ignition_period$start[z]),
                           "-ignition")
      sf::st_write(df_ignition, con, table_name)
      sql <- sprintf('
        insert into fleet_equipmentignitionstatus (
          equipment_id,
          time_stamp,
          ignition
        )
        select
          equipment_id,
          cast(time_stamp as timestamp) at time zone \'Asia/Manila\',
          ignition
        from "%s"
                     ', table_name)
      exec_retry(sql)
      sql <- sprintf('drop table "%s"', table_name)
      exec_retry(sql)

      df_tracker <- lapply(1:nrow(output), function(i) {
        data.frame(equipment_id = equipment_id,
                   time_stamp = output$time[i],
                   lng = output$location$lng[i],
                   lat = output$location$lat[i])
      }) %>%
        dplyr::bind_rows() %>%
        dplyr::group_by(equipment_id, time_stamp, lng, lat) %>%
        dplyr::summarise(lng = mean(lng), lat = mean(lat)) %>%
        sf::st_as_sf(coords = c("lng", "lat"))
      sf::st_write(df_tracker, con, table_name)
      sql <- sprintf('
        with cte_a as (
          select tab_a.*, tab_b.id
          from "%s" tab_a
          left join location_equipmentlocation tab_b
            on tab_a.equipment_id = tab_b.equipment_id
              and cast(tab_a.time_stamp as timestamp) at time zone \'Asia/Manila\' = tab_b.time_stamp
        )
        insert into location_equipmentlocation (
          equipment_id,
          time_stamp,
          geom
        )
        select
          equipment_id,
          cast(time_stamp as timestamp) at time zone \'Asia/Manila\',
          geometry
        from cte_a
        where id is null
                     ', table_name)
      exec_retry(sql)
      sql <- sprintf('drop table "%s"', table_name)
      exec_retry(sql)
    }
  }
})
