#!/usr/bin/bash

set -a
. data_management/local.py
set +a

if [ -f "log_upload_data" ]
then
    mv log_upload_data log_upload_data_$(date +"%Y-%m-%d_%H-%M-%S")
fi

echo "Uploading location_mineblock." && \
ogr2ogr -update -append -progress \
    -f PostgreSQL "PG:host=$db_host port=$db_port user=$db_user dbname=$db_name password=$db_password" \
    -fieldmap 0,1 \
    -nln location_mineblock data/location_mineblock.gpkg 2>&1 | tee -a log_upload_data && \
echo "Uploading inventory_block" && \
ogr2ogr -update -append -progress \
    -f PostgreSQL "PG:host=$db_host port=$db_port user=$db_user dbname=$db_name password=$db_password" \
    -fieldmap identity \
    -nln inventory_block data/inventory_block.gpkg 2>&1 | tee -a log_upload_data && \
./manage.py shell < scripts/upload_data/shipment_lct.py 2>&1 | tee -a log_upload_data && \
echo "Uploading shipment.LCT success." && \
./manage.py shell < scripts/upload_data/shipment_lctcontract.py 2>&1 | tee -a log_upload_data && \
echo "Uploading shipment.LCTContract success." && \
./manage.py shell < scripts/upload_data/shipment_vessel.py 2>&1 | tee -a log_upload_data && \
echo "Uploading shipment.Vessel success." && \
./manage.py shell < scripts/upload_data/shipment_shipment.py 2>&1 | tee -a log_upload_data && \
echo "Uploading shipment.Shipment success." && \
./manage.py shell < scripts/upload_data/shipment_laydaysstatement.py 2>&1 | tee -a log_upload_data && \
echo "Uploading shipment.LayDaysStatement success." && \
./manage.py shell < scripts/upload_data/shipment_laydaysdetail.py 2>&1 | tee -a log_upload_data && \
echo "Uploading shipment.LayDaysDetail success." && \
./manage.py shell < scripts/upload_data/shipment_trip.py 2>&1 | tee -a log_upload_data && \
echo "Uploading shipment.Trip success." && \
./manage.py shell < scripts/upload_data/shipment_tripdetail.py 2>&1 | tee -a log_upload_data && \
echo "Uploading shipment.TripDetail success."
