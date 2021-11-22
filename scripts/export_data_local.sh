#!/usr/bin/bash

set -a
. data_management/local.py
set +a

export datadir=data_local
export address=localhost:8000

export db_name
export db_user
export db_host
export db_port

source scripts/export_data_common.sh
