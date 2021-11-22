#!/usr/bin/bash

export datadir=data
export address=$DATA_MANAGEMENT_DB_HOST
export db_host=$DATA_MANAGEMENT_DB_HOST
export db_name=$DATA_MANAGEMENT_DB_NAME
export db_port=$DATA_MANAGEMENT_DB_PORT
export db_user=$DATA_MANAGEMENT_DB_USER

source scripts/export_data_common.sh
