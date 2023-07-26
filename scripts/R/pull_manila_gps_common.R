library(dplyr)
library(jsonlite)
library(lubridate)
library(RPostgres)

con <- RPostgres::dbConnect(RPostgres::Postgres(),
                            user = "data_management",
                            host = "datamanagement.tmc.nickelasia.com",
                            dbname = "data_management")

hash <- "hash=cb28e57165139a65de1e458737d2186d"
host <- "https://api.gpstrack.global/"

exec_retry <- function(x) {
  attempts <- 0L
  while(TRUE) {
    attempts <- attempts + 1L
    try_command <- tryCatch({
      RPostgres::dbExecute(con, x)
    }, error = function(err) {
      cat(paste("Error on attempt", attempts, ":", conditionMessage(err), "\n"))
      NULL
    })
    if (!is.null(try_command)) {
      return(try_command)
    }
    Sys.sleep(2)
  }
}

pull_retry <- function(x) {
  attempts <- 0L
  while (attempts <= 10L) {
    attempts <- attempts + 1L
    try_pull <- tryCatch({
      jsonlite::fromJSON(x)[[1]]
    }, error = function(err) {
      cat(paste("Error on attempt", attempts, ":", conditionMessage(err), "\n"))
      NULL
    })
    if (!is.null(try_pull)) {
      return(try_pull)
    }
    Sys.sleep(2)
  }
}

api_equipment_list <- paste0(host, "vehicle/list/?", hash)

gps_equipment_list <- jsonlite::fromJSON(api_equipment_list)[[1]] %>%
  dplyr::mutate(equipment_class = substr(tracker_label, 5L, 6L),
                fleet_number = as.integer(substr(tracker_label, 10L, 12L))) %>%
  dplyr::select(tracker_id, equipment_class, fleet_number)

dm_equipment <- RPostgres::dbGetQuery(con, "
select
  tab_a.id,
  tab_b.name equipment_class,
  tab_a.fleet_number
from fleet_equipment tab_a,
  fleet_equipmentclass tab_b,
  organization_organization tab_c
where tab_a.equipment_class_id = tab_b.id
  and tab_a.owner_id = tab_c.id
  and tab_c.name = 'TMC'
                                      ")
