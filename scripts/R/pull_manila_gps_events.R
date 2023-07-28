#!/usr/bin/Rscript

source("scripts/R/pull_manila_gps_common.R")

library(stringr)

equipment_list <- dplyr::left_join(gps_equipment_list, dm_equipment)

if (any(is.na(equipment_list$id))) {
  stop("Unregistered equipment detected.")
}

dates_included <- seq(from = as.Date("2023-02-01"),
                      to = as.Date("2023-07-27"),
                      by = "7 days")

ignition_period <- expand.grid(x = equipment_list$tracker_id,
                               y = dates_included,
                               KEEP.OUT.ATTRS = FALSE) %>%
  dplyr::mutate(id = dplyr::row_number())

lapply(1:nrow(ignition_period), function(z) {
  url <- paste0(
    host,
    "history/tracker/list/?trackers=[",
    ignition_period$x[z],
    "]&from=",
    ignition_period$y[z],
    "%2000:00:00&to=",
    ignition_period$y[z] + lubridate::days(6),
    "%2023:59:59&",
    hash
  )
  api_output <- pull_retry(url)
  cat(url, "\n")
  cat(sprintf("Processing %s out of %s.\n", z, nrow(ignition_period)))
  if (is.data.frame(api_output)) {
    equipment_id <- equipment_list$id[equipment_list$tracker_id == ignition_period$x[z]]
    output <- dplyr::filter(api_output,
                            stringr::str_detect(message, "Ignition")) %>%
      dplyr::arrange(time)
    if (nrow(output) > 0) {
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
      table_name <- paste0(ignition_period$x[z],
                           "-",
                           ignition_period$y[z],
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
