library(dplyr)
library(jsonlite)
library(lubridate)
library(RPostgres)
library(sf)
library(stringr)

con <- RPostgres::dbConnect(RPostgres::Postgres(),
                            user = "data_management",
                            host = "datamanagement.tmc.nickelasia.com",
                            dbname = "data_management")

hashes <- RPostgres::dbGetQuery(con, "
select a.key, b.name
from organization_manilagpsapikey a,
  organization_organization b
where a.owner_id = b.id
                                      ")

host <- "https://api.gpstrack.global/"
minimum_timestamp <-"2023-02-10 11:10:58+08"

print_log <- function(x, attempts, err) {
  cat(x,
      "\n",
      format(Sys.time(), "%Y-%m-%d %H:%M:%S"),
      "\n",
      paste("Error on attempt", attempts, ":", conditionMessage(err), "\n")
  )
}

exec_retry <- function(x) {
  attempts <- 0L
  while(TRUE) {
    attempts <- attempts + 1L
    try_command <- tryCatch({
      RPostgres::dbExecute(con, x)
    }, error = function(err) {
      print_log(x, attempts, err)
      NULL
    })
    if (attempts > 100)
      stop("Exceeded the number of attempts.")
    if (!is.null(try_command)) {
      return(try_command)
    }
    Sys.sleep(2)
  }
}

pull_retry <- function(x) {
  attempts <- 0L
  while (TRUE) {
    attempts <- attempts + 1L
    try_pull <- tryCatch({
      jsonlite::fromJSON(x)[[1]]
    }, error = function(err) {
      print_log(x, attempts, err)
      NULL
    })
    if (!is.null(try_pull)) {
      return(try_pull)
    }
    if (attempts > 100)
      stop("Exceeded the number of attempts.")
    Sys.sleep(2)
  }
}

data_set <- lapply(1:nrow(hashes), function(x) {
  api_equipment_list <- paste0(host, "vehicle/list/?hash=", hashes$key[x])
  owner <- hashes$name[x]
  pattern <- "[A-Z]+-([A-Z]+)\\d+-(\\d+)"
  mgps_equipment_list <- jsonlite::fromJSON(api_equipment_list)[[1]]

  # Print units with missing trackers:
  missing <- dplyr::filter(mgps_equipment_list, is.na(tracker_id))
  if (nrow(missing) > 0) {
    cat("GPS tracker IDs missing for", owner, ":\n")
    for (label in missing$label) {
      cat(paste0(label, "\n"))
    }
  }

  gps_equipment_list <- dplyr::filter(
    mgps_equipment_list,
    !is.na(tracker_id),
    stringr::str_detect(tracker_label, owner)
  ) %>%
    dplyr::mutate(
      tracker_label = stringr::str_remove_all(tracker_label, "\\s+")
    ) %>%
    dplyr::mutate(
      equipment_class = gsub(pattern, "\\1", tracker_label),
      fleet_number = as.integer(gsub(pattern, "\\2", tracker_label))
    ) %>%
    dplyr::select(tracker_id, equipment_class, fleet_number)

  query <- sprintf("
  select
  tab_a.id,
  tab_b.name equipment_class,
  tab_a.fleet_number
from fleet_equipment tab_a,
  fleet_equipmentclass tab_b,
  organization_organization tab_c
where tab_a.equipment_class_id = tab_b.id
  and tab_a.owner_id = tab_c.id
  and tab_c.name = '%s'
                   ", owner)
  dm_equipment <- RPostgres::dbGetQuery(con, query) %>%
    dplyr::right_join(gps_equipment_list)
  return(list(owner, gps_equipment_list, dm_equipment))
})

latest_point <- RPostgres::dbGetQuery(con, "
select equipment_id as id, max(time_stamp)
from location_equipmentlocation
group by equipment_id
                                      ") %>%
  dplyr::mutate(max = lubridate::with_tz(max, "Asia/Manila"))

