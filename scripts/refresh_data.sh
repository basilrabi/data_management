#!/usr/bin/bash

set -a
. data_management/local.py
set +a

upload_orm () {
    echo "Running $1 script." 2>&1 | tee -a log_upload_data && \
    time_start=$(date +%s) && \
    python3 manage.py shell < scripts/upload_data/$1.py 2>&1 | tee -a log_upload_data && \
    time_end=$(date +%s) && \
    time_elapsed=$(($time_end - $time_start)) && \
    echo "orm $1, $time_elapsed" >> log_upload_data_time.csv
}

upload_orm shipment_laydaysdetail && \
upload_orm shipment_tripdetail
