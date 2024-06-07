#!/usr/bin/bash

set -a
. data_management/local.py
set +a

lftp -c mirror  http://datamanagement.tmc.nickelasia.com:81/applications/data_management_export data
./scripts/clean_db.sh
./scripts/upload_data.sh

