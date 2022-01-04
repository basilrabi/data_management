#!/usr/bin/Rscript

db_host <- Sys.getenv("db_host")
db_name <- Sys.getenv("db_name")
db_password <- Sys.getenv("db_password")
db_port <- Sys.getenv("db_port")
db_user <- Sys.getenv("db_user")

external_tables <- read.csv("data/external_tables/tables.csv")

psql <- function(db_host,
                 db_user,
                 db_name,
                 query,
                 ignore.stdout = TRUE,
                 use_single_quoute = TRUE) {
  cmd <- paste0("psql -h ", db_host, " -U ", db_user, " -d ", db_name, " -c")
  if (use_single_quoute) {
    cmd <- paste0(cmd, "'", query, "'")
  } else {
    cmd <- paste0(cmd, '"', query, '"')
  }
  if (system(cmd, ignore.stdout = ignore.stdout) != 0)
    stop("PSQL command error.")

  return(invisible(NULL))
}

upload_ogr <- function(schema_name, table_name, file_name, table_owner) {
  cmd <- sprintf(
    'ogr2ogr -update -append -progress -f PostgreSQL "PG:host=%s port=%s user=%s dbname=%s password=%s" -fieldmap "%s" -lco LAUNDER=NO -nln "%s"."%s" data/external_tables/%s.gpkg',
    db_host,
    db_port,
    db_user,
    db_name,
    db_password,
    "identity",
    schema_name,
    table_name,
    file_name
  )
  cat(cmd, "\n")
  if (system(cmd) != "0")
    stop("ogr2ogr error.")

  if (!table_owner %in% c("", "data_management")) {
    cmd <- sprintf(
      'ALTER TABLE \"%s\".\"%s\" OWNER TO %s',
      schema_name, table_name, table_owner
    )
    cat(cmd, "\n")
    psql(db_host, db_user, db_name, cmd)
  }

  return(invisible(NULL))
}

for (i in 1:nrow(external_tables)) {
  upload_ogr(external_tables$table_schema[i],
             external_tables$table_name[i],
             external_tables$valid_name[i],
             external_tables$table_owner[i])
}
