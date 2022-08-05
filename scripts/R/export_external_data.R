#!/usr/bin/Rscript

library(DBI)
library(RPostgres)
library(dplyr)

datadir <- Sys.getenv("datadir")
db_host <- Sys.getenv("db_host")
db_name <- Sys.getenv("db_name")
db_user <- Sys.getenv("db_user")
db_port <- as.integer(Sys.getenv("db_port"))

download_ogr <- function(schema_name, table_name, valid_file_name) {
  cmd <- sprintf(
    'ogr2ogr -f "GPKG" %s/external_tables/"%s.gpkg" "PG:host=%s user=%s dbname=%s" "%s"."%s"',
    datadir, valid_file_name, db_host, db_user, db_name, schema_name, table_name
  )
  cat(cmd, "\n")
  if (system(cmd) != "0")
    stop("ogr2ogr error.")
  return(invisible(NULL))
}

con <- DBI::dbConnect(RPostgres::Postgres(),
                      dbname = db_name,
                      host = db_host,
                      port = db_port,
                      user = db_user)

# Get non-standard tables

query <- "
select
  a.table_schema,
  a.table_name,
  b.tableowner table_owner
from information_schema.tables a
left join pg_tables b
  on a.table_schema = b.schemaname
    and a.table_name = b.tablename
where a.table_type = 'BASE TABLE'
    and a.table_schema not in ('information_schema', 'pg_catalog')
    and not a.table_name ilike any (array[
        'auth_%',
        'billing_%',
        'comptrollership_%',
        'custom_%',
        'django_%',
        'fleet_%',
        'gammu',
        'inbox',
        'inventory_%',
        'local_calendar_%',
        'location_%',
        'material_management_%'
        'organization_%',
        'outbox',
        'outbox_multipart',
        'personnel_%',
        'phones',
        'sampling_%',
        'sentitems',
        'shipment_%',
        'spatial_ref_sys',
        'surface_green',
        'surface_lower',
        'surface_upper',
        'temp_ply_%'
    ])
order by a.table_schema, a.table_name
"

external_tables <- RPostgres::dbGetQuery(conn = con, statement = query) %>%
  dplyr::mutate(
    table_owner = dplyr::case_when(table_owner == db_user ~ as.character(NA),
                                   TRUE ~ table_owner),
    valid_name = paste(table_schema,
                       gsub("/|\\s+", "", table_name),
                       sep = "-")
  )

if (any(duplicated(external_tables$valid_name)))
  stop("Duplicated name exists.")

if (!dir.exists(paste0(datadir, "/external_tables")))
  dir.create(paste0(datadir, "/external_tables"))

write.csv(external_tables,
          file = paste0(datadir, "/external_tables/tables.csv"),
          row.names = FALSE,
          na = "")

for (i in 1:nrow(external_tables)) {
  download_ogr(external_tables$table_schema[i],
               external_tables$table_name[i],
               external_tables$valid_name[i])
}
