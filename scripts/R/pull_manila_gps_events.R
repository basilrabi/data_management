#!/usr/bin/Rscript

begin <- Sys.time()

source("scripts/R/pull_manila_gps_common.R")

latest_idle <- RPostgres::dbGetQuery(con, "
select equipment_id id,
    max(time_stamp) time_stamp
from fleet_equipmentidlingtime
group by equipment_id
                                         ") %>%
  dplyr::mutate(time_stamp = lubridate::with_tz(time_stamp, "Asia/Manila"))

dummy <- lapply(1:length(data_set), function(idx) {
  equipment_list <- data_set[[idx]][[3]] %>%
    dplyr::rename(equipment_id = id) %>%
    dplyr::select(equipment_id, tracker_id) %>%
    dplyr::filter(!is.na(equipment_id))
  RPostgres::dbWriteTable(con, "staging_tracker_id",
                          equipment_list,
                          overwrite = TRUE)
  sql <- "
  with cte_a as (
    select equipment_id, tracker_id
    from staging_tracker_id
    where equipment_id not in (
      select equipment_id
      from location_manilagpswebsocketdata
    )
  )
  insert into location_manilagpswebsocketdata (equipment_id, tracker_id)
  select equipment_id, tracker_id
  from cte_a
  "
  rows <- exec_retry(sql)
  if (rows > 0) {
    cat(sprintf("Inserted %i new trackers from %s.\n", rows, hashes$name[idx]))
  }

  sql <- "
  update location_manilagpswebsocketdata
  set tracker_id = staging_tracker_id.tracker_id
  from staging_tracker_id
  where location_manilagpswebsocketdata.equipment_id = staging_tracker_id.equipment_id
    and location_manilagpswebsocketdata.tracker_id <> staging_tracker_id.tracker_id
  "
  rows <- exec_retry(sql)
  if (rows > 0) {
    cat(sprintf("Updated %i trackers from %s.\n", rows, hashes$name[idx]))
  }

  invisible(NULL)
})
sql <- "drop table if exists staging_tracker_id"
exec_retry(sql)

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

dummy <- lapply(1:length(data_set), function(idx) {
  owner <- data_set[[idx]][[1]]
  dm_equipment <- data_set[[idx]][[3]]
  if (any(is.na(dm_equipment$id))) {
    cat(sprintf("WARNING. Unregistered equipment detected for %s:\n", owner))
    unregistered <- dplyr::filter(dm_equipment, is.na(id)) %>%
      dplyr::mutate(unit = sprintf(
        "%s-%s-%03i", owner, equipment_class, fleet_number
      ))
    cat(paste(unregistered$unit, collapse = "\n"), "\n")
    dm_equipment <- dplyr::filter(dm_equipment, !is.na(id))
  }

  equipment_list <- dplyr::left_join(dm_equipment,
                                     latest_point,
                                     by = c("id")) %>%
    dplyr::left_join(latest_status, by = c("id")) %>%
    dplyr::mutate(start = dplyr::case_when(
      !is.na(max_status) ~ max_status,
      TRUE ~ as.POSIXct(minimum_timestamp)
    )) %>%
    dplyr::filter(start < max)

  if (nrow(equipment_list) > 0) {
    file_inactive <- sprintf("/home/datamanagement/media/static/TMC/inactive_gps_%s.csv", owner)
    if (nrow(equipment_list) < nrow(dm_equipment)) {
      inactive <- dplyr::left_join(dm_equipment,
                                   latest_point,
                                   by = c("id")) %>%
        dplyr::left_join(latest_status, by = c("id")) %>%
        dplyr::mutate(
          start = dplyr::case_when(
            !is.na(max_status) & !is.na(max) & (max_status > max)  ~ max_status,
            !is.na(max_status) & !is.na(max) & (max > max_status)  ~ max,
            !is.na(max_status) ~ max_status,
            !is.na(max) ~ max,
            TRUE ~ as.POSIXct(minimum_timestamp)
          ),
          now = Sys.time()
        ) %>%
        dplyr::mutate(diff = as.numeric(difftime(now, start, units = "days"))) %>%
        dplyr::filter(diff >= 7)
      if (nrow(inactive) > 0) {
        write.csv(inactive, file_inactive)
      }
    } else {
      if (file.exists(file_inactive))
        file.remove(file_inactive)
    }

    events_period <- lapply(1:nrow(equipment_list), function(x) {
      data.frame(
        tracker_id = equipment_list$tracker_id[x],
        start = seq(from = equipment_list$start[x],
                    to = equipment_list$max[x],
                    by = "7 days")
      )
    }) %>%
      dplyr::bind_rows() %>%
      dplyr::left_join(dplyr::select(equipment_list, tracker_id, max),
                       by = c("tracker_id")) %>%
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
        "&hash=",
        hashes$key[idx]
      )
      api_output <- pull_retry(url)
      if (debug)
        cat(sprintf("Processing %s out of %s.\n", z, nrow(events_period)))
      if (is.data.frame(api_output)) {
        equipment_id <- equipment_list$id[equipment_list$tracker_id == events_period$tracker_id[z]]
        if (debug)
          cat(url, "\n")
        if (nrow(api_output) > 99) {
          while (TRUE) {
            if (debug)
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
              if (debug)
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
          insert_count <- exec_retry(sql)
          if (debug)
            cat("Inserted", insert_count, "for idling.\n")
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
            as.data.frame() %>%
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
          insert_count <- exec_retry(sql)
          if (debug)
            cat("Inserted", insert_count, "for idling location.\n")
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
          insert_count <- exec_retry(sql)
          if (debug)
            cat("Inserted", insert_count, "for ignition status.\n")
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
            as.data.frame() %>%
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
          insert_count <- exec_retry(sql)
          if (debug)
            cat("Inserted", insert_count, "for ignition status location.\n")
          sql <- sprintf('drop table "%s"', table_name)
          exec_retry(sql)
        }
      }
      invisible(NULL)
    })
  }
  invisible(NULL)
})


exec_retry("vacuum analyze fleet_equipmentidlingtime")
exec_retry("vacuum analyze fleet_equipmentignitionstatus")

if (debug)
  cat("Refreshing fleet_equipmentignitioninterval")
exec_retry("refresh materialized view concurrently fleet_equipmentignitioninterval")
exec_retry("vacuum analyze fleet_equipmentignitioninterval")

if (debug)
  cat("Refreshing fleet_equipmentidlinginterval")
exec_retry("refresh materialized view concurrently fleet_equipmentidlinginterval")
exec_retry("vacuum analyze fleet_equipmentidlinginterval")

if (debug)
  cat("Refreshing dash_equipmentusage")
exec_retry("refresh materialized view concurrently dash_equipmentusage")
exec_retry("vacuum analyze dash_equipmentusage")

end <- Sys.time()
time_elapsed <- end - begin
cat("Finished in", format(time_elapsed), "\n")

