#!/usr/bin/Rscript

begin <- Sys.time()

source("scripts/R/pull_manila_gps_common.R")

library(stringr)

if (any(is.na(dm_equipment$id))) {
  stop("Unregistered equipment detected.")
}

latest_idle <- RPostgres::dbGetQuery(con, "
select equipment_id id,
    max(time_stamp) time_stamp
from fleet_equipmentidlingtime
group by equipment_id
                                         ") %>%
  dplyr::mutate(time_stamp = lubridate::with_tz(time_stamp, "Asia/Manila"))

latest_ignition <- RPostgres::dbGetQuery(con, "
select equipment_id id,
    max(time_stamp) time_stamp
from fleet_equipmentignitionstatus
group by equipment_id
                                         ") %>%
  dplyr::mutate(time_stamp = lubridate::with_tz(time_stamp, "Asia/Manila"))

latest_status <- dplyr::bind_rows(latest_idle, latest_ignition) %>%
  dplyr::group_by(id) %>%
  dplyr::summarise(max_status = max(time_stamp))

equipment_list <- dplyr::left_join(dm_equipment, latest_point) %>%
  dplyr::left_join(latest_status) %>%
  dplyr::mutate(start = dplyr::case_when(
    !is.na(max_status) ~ max_status,
    TRUE ~ as.POSIXct(minimum_timestamp)
  )) %>%
  dplyr::filter(start < max)

events_period <- lapply(1:nrow(equipment_list), function(x) {
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

lapply(1:nrow(events_period), function(z) {
  url <- paste0(
    host,
    "history/tracker/list/?trackers=[",
    events_period$tracker_id[z],
    "]&from=",
    format(events_period$start[z], format = "%Y-%m-%d%%20%H:%M:%S"),
    "&to=",
    format(events_period$end[z], format = "%Y-%m-%d%%20%H:%M:%S"),
    "&",
    hash
  )
  api_output <- pull_retry(url)
  cat(sprintf("Processing %s out of %s.\n", z, nrow(events_period)))
  if (is.data.frame(api_output)) {
    equipment_id <- equipment_list$id[equipment_list$tracker_id == events_period$tracker_id[z]]
    cat(url, "\n")
    if (nrow(api_output) > 99) {
      while (TRUE) {
        cat("History limit reached. Fetching new datetime range.\n")
        new_from <- as.POSIXct(sprintf("%s+8", max(api_output$time))) %>%
          format(format = "%Y-%m-%d%%20%H:%M:%S")
        new_url <- stringr::str_replace(
          url,
          "from=\\d{4}-\\d{2}-\\d{2}%20\\d{2}:\\d{2}:\\d{2}",
          sprintf("from=%s", new_from)
        )
        additional_output <- pull_retry(new_url)
        if (is.data.frame(additional_output)) {
          master <- api_output[nrow(api_output), "id"]
          additional <- additional_output[nrow(additional_output), "id"]
          if (master == additional)
            break
          cat(new_url, "\n")
          api_output <- dplyr::bind_rows(api_output, additional_output)
        } else {
          break
        }
      }
    }

    # idling
    output <- dplyr::filter(api_output,
                            stringr::str_detect(event, "idle")) %>%
      dplyr::arrange(time)
    if (nrow(output) > 0) {
      df_idle <- lapply(1:nrow(output), function(i) {
        data.frame(equipment_id = equipment_id,
                   time_stamp = output$time[i],
                   idling = stringr::str_detect(output$event[i], "idle_start"))
      }) %>%
        dplyr::bind_rows() %>%
        dplyr::group_by(equipment_id, time_stamp, idling) %>%
        dplyr::summarise() %>%
        dplyr::group_by(time_stamp) %>%
        dplyr::mutate(n = dplyr::n()) %>%
        dplyr::filter(n < 2)
      table_name <- paste0(events_period$tracker_id[z],
                           "-",
                           as.Date(events_period$start[z]),
                           "-idle")
      sf::st_write(df_idle, con, table_name)
      sql <- sprintf('
        with cte_a as (
          select tab_a.equipment_id,
            cast(tab_a.time_stamp as timestamp) at time zone \'Asia/Manila\' as ts,
            tab_a.idling,
            tab_b.id
          from "%s" tab_a
          left join fleet_equipmentidlingtime tab_b
            on tab_a.equipment_id = tab_b.equipment_id
              and cast(tab_a.time_stamp as timestamp) at time zone \'Asia/Manila\' = tab_b.time_stamp
        )
        insert into fleet_equipmentidlingtime (
          equipment_id,
          time_stamp,
          idling
        )
        select
          equipment_id,
          ts,
          idling
        from cte_a
        where id is null
                     ', table_name)
      cat("Inserted", exec_retry(sql), "for idling.\n")
      sql <- sprintf('drop table "%s"', table_name)
      exec_retry(sql)

      df_tracker <- lapply(1:nrow(output), function(i) {
        data.frame(equipment_id = equipment_id,
                   time_stamp = output$time[i],
                   lng = output$location$lng[i],
                   lat = output$location$lat[i])
      }) %>%
        dplyr::bind_rows() %>%
        dplyr::group_by(equipment_id, time_stamp) %>%
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
      cat("Inserted", exec_retry(sql), "for idling location.\n")
      sql <- sprintf('drop table "%s"', table_name)
      exec_retry(sql)
    }

    # ignition
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
      table_name <- paste0(events_period$tracker_id[z],
                           "-",
                           as.Date(events_period$start[z]),
                           "-ignition")
      sf::st_write(df_ignition, con, table_name)
      sql <- sprintf('
        with cte_a as (
          select tab_a.equipment_id,
            cast(tab_a.time_stamp as timestamp) at time zone \'Asia/Manila\' as ts,
            tab_a.ignition,
            tab_b.id
          from "%s" tab_a
          left join fleet_equipmentignitionstatus tab_b
            on tab_a.equipment_id = tab_b.equipment_id
              and cast(tab_a.time_stamp as timestamp) at time zone \'Asia/Manila\' = tab_b.time_stamp
        )
        insert into fleet_equipmentignitionstatus (
          equipment_id,
          time_stamp,
          ignition
        )
        select
          equipment_id,
          ts,
          ignition
        from cte_a
        where id is null
                     ', table_name)
      cat("Inserted", exec_retry(sql), "for ignition status.\n")
      sql <- sprintf('drop table "%s"', table_name)
      exec_retry(sql)

      df_tracker <- lapply(1:nrow(output), function(i) {
        data.frame(equipment_id = equipment_id,
                   time_stamp = output$time[i],
                   lng = output$location$lng[i],
                   lat = output$location$lat[i])
      }) %>%
        dplyr::bind_rows() %>%
        dplyr::group_by(equipment_id, time_stamp) %>%
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
      cat("Inserted", exec_retry(sql), "for ignition status location.\n")
      sql <- sprintf('drop table "%s"', table_name)
      exec_retry(sql)
    }
  }
})

exec_retry("vacuum analyze fleet_equipmentidlingtime")
exec_retry("vacuum analyze fleet_equipmentignitionstatus")

cat("Refreshing fleet_equipmentignitioninterval")
exec_retry("refresh materialized view concurrently fleet_equipmentignitioninterval")
exec_retry("vacuum analyze fleet_equipmentignitioninterval")

cat("Refreshing fleet_equipmentidlinginterval")
exec_retry("refresh materialized view concurrently fleet_equipmentidlinginterval")
exec_retry("vacuum analyze fleet_equipmentidlinginterval")

cat("Refreshing dash_equipmentusage")
exec_retry("refresh materialized view concurrently dash_equipmentusage")
exec_retry("vacuum analyze dash_equipmentusage")

end <- Sys.time()
time_elapsed <- end - begin
cat("Finished in", format(time_elapsed), "\n")

