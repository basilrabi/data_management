#!/usr/bin/Rscript

library(DBI)
library(RPostgres)
library(dplyr)
library(tmctools)

db_host <- Sys.getenv("DATA_MANAGEMENT_DB_HOST")
db_name <- Sys.getenv("DATA_MANAGEMENT_DB_NAME")
db_user <- Sys.getenv("DATA_MANAGEMENT_DB_USER")

download_ogr <- function(schema_name, table_name, valid_file_name) {
  cmd <- sprintf(
    'ogr2ogr -f "GPKG" data/external_tables/"%s-%s.gpkg" "PG:host=%s user=%s dbname=%s" "%s"."%s"',
    schema_name, valid_file_name, db_host, db_user, db_name, schema_name, table_name
  )
  cat(cmd, "\n")
  if (system(cmd) != "0")
    stop("ogr2ogr error.")
  return(invisible(NULL))
}

sql <- function(x) {
  tmctools::psql(db_host, db_user, db_name, x)
}

con <- DBI::dbConnect(RPostgres::Postgres(),
                      dbname = db_name,
                      host = db_host,
                      port = 5432,
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
        'controllership_%',
        'custom_user%',
        'django_%',
        'fleet_%',
        'inventory_%',
        'location_%',
        'personnel_%',
        'sampling_%',
        'shipment_%',
        'spatial_ref_sys'
    ])
order by a.table_schema, a.table_name
"

external_tables <- RPostgres::dbGetQuery(conn = con, statement = query) %>%
  dplyr::mutate(valid_name = gsub("/", "", table_name))

if (!dir.exists("data/external_tables"))
  dir.create("data/external_tables")

write.csv(external_tables,
          file = "data/external_tables/tables.csv",
          row.names = FALSE)

for (i in 1:nrow(external_tables)) {
  download_ogr(external_tables$table_schema[i],
               external_tables$table_name[i],
               external_tables$valid_name[i])
}
