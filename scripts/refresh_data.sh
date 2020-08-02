#!/usr/bin/bash

set -a
. data_management/local.py
set +a

 source scripts/functions.sh

upload_orm shipment_laydaysdetail && \
upload_orm shipment_tripdetail && \
sql_script "upload_data" "shipment_approvedlaydaysstatement" && \
vacuum "shipment_approvedlaydaysstatement"
