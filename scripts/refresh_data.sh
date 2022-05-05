#!/usr/bin/bash

source $HOME/.virtualenvs/data_management/bin/activate

set -a
. data_management/local.py
set +a

source scripts/functions.sh

sql_script "upload_data" "insert_shipment_approvedlaydaysstatement" && \
vacuum "shipment_approvedlaydaysstatement" && \
sql_script "upload_data" "shipment_approvedlaydaysstatement" && \
vacuum "shipment_approvedlaydaysstatement"
