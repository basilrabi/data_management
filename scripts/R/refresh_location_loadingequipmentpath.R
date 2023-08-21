#!/usr/bin/Rscript

if (file.exists("refresh_location_loadingequipmentpath.lock"))
  stop("Running process exists.")

file.create("refresh_location_loadingequipmentpath.lock")

begin <- Sys.time()

source("scripts/R/pull_manila_gps_common.R")
exec_retry("refresh materialized view concurrently location_loadingequipment")
exec_retry("vacuum analyze location_loadingequipment")
exec_retry("refresh materialized view concurrently location_loadingequipmentpath")
exec_retry("vacuum analyze location_loadingequipmentpath")

end <- Sys.time()
time_elapsed <- end - begin
cat("Finished in", format(time_elapsed), "\n")

file.remove("refresh_location_loadingequipmentpath.lock")

