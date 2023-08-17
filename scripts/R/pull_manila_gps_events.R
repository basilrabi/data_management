#!/usr/bin/Rscript

source("scripts/R/pull_manila_gps_common.R")

library(stringr)

if (any(is.na(dm_equipment$id))) {
  stop("Unregistered equipment detected.")
}

equipment_list <- dplyr::left_join(dm_equipment, latest_point) %>%
  dplyr::mutate(start = max(as.POSIXct(minimum_timestamp), max - lubridate::years())) %>%
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

    # idling
    output <- dplyr::filter(api_output,
                            stringr::str_detect(event, "idle")) %>%
      dplyr::arrange(time)
    if (nrow(output) > 0) {
      cat(url, "\n")

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
