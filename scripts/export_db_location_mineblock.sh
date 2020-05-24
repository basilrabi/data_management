#!/usr/bin/bash

db_host=$DATA_MANAGEMENT_DB_HOST
db_name=$DATA_MANAGEMENT_DB_NAME
db_user=$DATA_MANAGEMENT_DB_USER

pg_dump -h $db_host -U $db_user \
    --table=location_mineblock --data-only --column-inserts \
    $db_name | \
    grep "INSERT INTO" \
    > scripts/sql/dump/location_mineblock.pgsql
