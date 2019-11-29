#!/usr/bin/bash

if [ -d "data" ]
then
    mv data data_$(date +"%Y-%m-%d_%H-%M-%S")
fi
mkdir data

mv data_management/local.py data_management/local.py.bak
cat >data_management/local.py <<EOL
db_name = '$DATA_MANAGEMENT_DB_NAME'
db_user = '$DATA_MANAGEMENT_DB_USER'
db_password = '$DATA_MANAGEMENT_DB_PASSWORD'
db_host = '$DATA_MANAGEMENT_DB_HOST'
db_port = '$DATA_MANAGEMENT_DB_PORT'
EOL

ogr2ogr -f "GPKG" data/location_mineblock.gpkg \
    "PG:host=$DATA_MANAGEMENT_DB_HOST user=$DATA_MANAGEMENT_DB_USER dbname=$DATA_MANAGEMENT_DB_NAME" \
    location_mineblock

./manage.py shell < scripts/export_data/shipment_lct.py
./manage.py shell < scripts/export_data/shipment_lctcontract.py
./manage.py shell < scripts/export_data/shipment_vessel.py
./manage.py shell < scripts/export_data/shipment_shipment.py
./manage.py shell < scripts/export_data/shipment_trip.py
./manage.py shell < scripts/export_data/shipment_tripdetail.py

mv data_management/local.py.bak data_management/local.py
