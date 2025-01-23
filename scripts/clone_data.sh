#!/usr/bin/bash

set -a
. data_management/local.py
set +a

if [ -z "${datadir}" ]; then
    echo "The variable 'datadir' is not defined. Data clone aborted."
    exit 1
fi

lftp -c mirror http://datamanagement.tmc.nickelasia.com:81/applications/data_management_export $datadir
lftp -c mirror http://datamanagement.tmc.nickelasia.com:81/uploads/ ${DATA_MANAGEMENT_MEDIA_ROOT%/}
./scripts/clean_db.sh
./scripts/upload_data.sh

