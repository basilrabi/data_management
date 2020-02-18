#!/usr/bin/bash

set -a
. data_management/local.py
set +a

if [ -f "log_upload_data" ]
then
    mv log_upload_data log_upload_data_$(date +"%Y-%m-%d_%H-%M-%S")
fi

echo "Uploading location_mineblock." 2>&1 | tee -a log_upload_data && \
ogr2ogr -update -append -progress \
    -f PostgreSQL "PG:host=$db_host port=$db_port user=$db_user dbname=$db_name password=$db_password" \
    -fieldmap identity \
    -nln location_mineblock data/location_mineblock.gpkg 2>&1 | tee -a log_upload_data && \
./manage.py shell < scripts/upload_data/inventory_block.py 2>&1 | tee -a log_upload_data && \
echo "Uploading inventory.Block success." 2>&1 | tee -a log_upload_data && \
./manage.py shell < scripts/upload_data/location_cluster.py 2>&1 | tee -a log_upload_data && \
echo "Uploading location.Cluster success." 2>&1 | tee -a log_upload_data && \
./manage.py shell < scripts/upload_data/shipment_lct.py 2>&1 | tee -a log_upload_data && \
echo "Uploading shipment.LCT success." 2>&1 | tee -a log_upload_data && \
./manage.py shell < scripts/upload_data/shipment_lctcontract.py 2>&1 | tee -a log_upload_data && \
echo "Uploading shipment.LCTContract success." 2>&1 | tee -a log_upload_data && \
./manage.py shell < scripts/upload_data/shipment_vessel.py 2>&1 | tee -a log_upload_data && \
echo "Uploading shipment.Vessel success." 2>&1 | tee -a log_upload_data && \
./manage.py shell < scripts/upload_data/shipment_shipment.py 2>&1 | tee -a log_upload_data && \
echo "Uploading shipment.Shipment success." 2>&1 | tee -a log_upload_data && \
./manage.py shell < scripts/upload_data/shipment_laydaysstatement.py 2>&1 | tee -a log_upload_data && \
echo "Uploading shipment.LayDaysStatement success." 2>&1 | tee -a log_upload_data && \
./manage.py shell < scripts/upload_data/shipment_laydaysdetail.py 2>&1 | tee -a log_upload_data && \
echo "Uploading shipment.LayDaysDetail success." 2>&1 | tee -a log_upload_data && \
./manage.py shell < scripts/upload_data/shipment_trip.py 2>&1 | tee -a log_upload_data && \
echo "Uploading shipment.Trip success." 2>&1 | tee -a log_upload_data && \
./manage.py shell < scripts/upload_data/shipment_tripdetail.py 2>&1 | tee -a log_upload_data && \
echo "Uploading shipment.TripDetail success." 2>&1 | tee -a log_upload_data && \
./manage.py shell < scripts/upload_data/groups.py 2>&1 | tee -a log_upload_data && \
echo "Uploading Groups success." 2>&1 | tee -a log_upload_data && \
./manage.py shell < scripts/upload_data/users.py 2>&1 | tee -a log_upload_data && \
echo "Uploading Users success." 2>&1 | tee -a log_upload_data && \
echo "Adding postgres triggers..." 2>&1 | tee -a log_upload_data && \
psql -h $db_host -p $db_port -U tmcgis -w $db_name -a -f scripts/sql/function/get_ore_class.pgsql && \
psql -h $db_host -p $db_port -U tmcgis -w $db_name -a -f scripts/sql/trigger/location_cluster_update.pgsql && \
echo "Done." 2>&1 | tee -a log_upload_data
