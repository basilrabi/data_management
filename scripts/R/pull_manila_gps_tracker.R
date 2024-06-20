#!/usr/bin/Rscript

begin <- Sys.time()

source("scripts/R/pull_manila_gps_common.R")

dummy <- lapply(1:length(data_set), function(idx) {
  owner <- data_set[[idx]][[1]]
  equipment_list <- dplyr::left_join(
    data_set[[idx]][[3]],
    dplyr::mutate(latest_point, max = max + lubridate::seconds(1)),
    by = c("id")
  ) %>%
    dplyr::mutate(max = dplyr::case_when(
      is.na(max) ~ as.POSIXct(minimum_timestamp),
      TRUE ~ max
    ))

  if (any(is.na(equipment_list$id))) {
    cat(sprintf("WARNING. Unregistered equipment detected for %s:\n", owner))
    unregistered <- dplyr::filter(equipment_list, is.na(id)) %>%
      dplyr::mutate(unit = sprintf(
        "%s-%s-%03i", owner, equipment_class, fleet_number
      ))
    cat(paste(unregistered$unit, collapse = "\n"), "\n")
    equipment_list <- dplyr::filter(equipment_list, !is.na(id))
  }

  now <- Sys.time()
  tracker_period <- lapply(1:nrow(equipment_list), function(x) {
    data.frame(
      x = equipment_list$tracker_id[x],
      y = seq(from = equipment_list$max[x],
              to = now,
              by = "7 days")
    )
  }) %>%
    dplyr::bind_rows()

  lapply(1:nrow(tracker_period), function(z) {
    url <- paste0(
      host,
      "track/read/?simplify=false&tracker_id=",
      tracker_period$x[z],
      "&from=",
      format(tracker_period$y[z], format = "%Y-%m-%d%%20%H:%M:%S"),
      "&to=",
      format(tracker_period$y[z] + lubridate::days(7) - lubridate::seconds(1),
             format = "%Y-%m-%d%%20%H:%M:%S"),
      "&hash=",
      hashes$key[idx]
    )
    api_output <- pull_retry(url)
    if (debug)
      cat(sprintf("Processing %s out of %s.\n", z, nrow(tracker_period)))
    if (is.data.frame(api_output)) {
      if (debug)
        cat(url, "\n")
      equipment_id <- equipment_list$id[equipment_list$tracker_id == tracker_period$x[z]]
      output <- sf::st_as_sf(api_output, coords = c("lng", "lat")) %>%
        dplyr::select(time_stamp = get_time,
                      satellites,
                      heading,
                      speed) %>%
        dplyr::arrange(time_stamp)
      output$id <- 1:nrow(output)
      table_name <- paste0(tracker_period$x[z], "-", tracker_period$y[z])
      sf::st_write(output, con, table_name)
      sql <- sprintf("select UpdateGeometrySRID('public', '%s', 'geometry', 4326)", table_name)
      exec_retry(sql)
      sql <- sprintf('alter table "%s" add unique(id)', table_name)
      exec_retry(sql)
      sql <- sprintf('vacuum analyze "%s"', table_name)
      exec_retry(sql)
      sql <- sprintf('
      with cte_a as (
        select
          tab_a.time_stamp,
          tab_a.satellites,
          tab_a.heading,
          tab_a.speed,
          tab_a.geometry,
          previous_point.heading as pp_heading,
          previous_point.speed as pp_speed,
          previous_point.geometry as pp_geom,
          next_point.heading as np_heading,
          next_point.speed as np_speed,
          next_point.geometry as np_geom
        from "%s" as tab_a
        left join lateral (
          select *
          from "%s" as tab_b
          where tab_a.id > tab_b.id
          order by tab_b.id desc
          limit 1
        ) previous_point on true
        left join lateral (
          select *
          from "%s" as tab_b
          where tab_a.id < tab_b.id
          order by tab_b.id asc
          limit 1
        ) next_point on true
      ),
      cte_b as (
        select
          time_stamp,
          satellites,
          heading,
          speed,
          geometry as geom,
          case
            when pp_heading is null then true
            when np_heading is null then true
            when (
              speed = 0 and
              pp_speed = 0 and
              np_speed = 0 and
              pp_heading = heading and
              np_heading = heading and
              st_distance(geometry, pp_geom) < 1 and
              st_distance(geometry, np_geom) < 1
            ) then false
            else true
          end as included
        from cte_a
      ),
      cte_c as (
        select
          time_stamp,
          avg(satellites)::int as satellites,
          avg(heading)::int as heading,
          avg(speed)::int as speed,
          st_centroid(st_union(geom)) as geom
        from cte_b
        where included
        group by time_stamp
      )
      insert into location_equipmentlocation(
        equipment_id,
        time_stamp,
        satellites,
        heading,
        speed,
        geom
      )
      select
        %s,
        cast(time_stamp as timestamp) at time zone \'Asia/Manila\',
        case
          when satellites > -1 then satellites
          else null
        end,
        heading,
        speed,
        geom
      from cte_c', table_name, table_name, table_name, equipment_id)
      insert_count <- exec_retry(sql)
      if (debug)
        cat("Inserted", insert_count, "new equipment locations.\n")
      sql <- sprintf('drop table "%s"', table_name)
      exec_retry(sql)
    }
    invisible(NULL)
  })
  invisible(NULL)
})

exec_retry("vacuum analyze location_equipmentlocation")

end <- Sys.time()
time_elapsed <- end - begin
cat("Finished in", format(time_elapsed), "\n")
