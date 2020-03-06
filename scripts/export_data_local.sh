#!/usr/bin/bash

set -a
. data_management/local.py
set +a

datadir=data_local
address=localhost:8000

source scripts/export_data_common.sh
