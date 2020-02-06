#!/usr/bin/bash

if [ -d "data" ]
then
    mv data data_$(date +"%Y-%m-%d_%H-%M-%S")
fi
mkdir data

ogr2ogr -progress -f "GPKG" data/location_mineblock.gpkg \
    "PG:host=$DATA_MANAGEMENT_DB_HOST user=$DATA_MANAGEMENT_DB_USER dbname=$DATA_MANAGEMENT_DB_NAME" \
    location_mineblock

ogr2ogr -progress -f "GPKG" data/inventory_block.gpkg \
    "PG:host=$DATA_MANAGEMENT_DB_HOST user=$DATA_MANAGEMENT_DB_USER dbname=$DATA_MANAGEMENT_DB_NAME" \
    inventory_block

curl datamanagement.tmc.nickelasia.com/shipment/export/lct -o data/shipment_lct.csv
curl datamanagement.tmc.nickelasia.com/shipment/export/lctcontract -o data/shipment_lctcontract.csv
curl datamanagement.tmc.nickelasia.com/shipment/export/vessel -o data/shipment_vessel.csv
curl datamanagement.tmc.nickelasia.com/shipment/export/shipment -o data/shipment_shipment.csv
curl datamanagement.tmc.nickelasia.com/shipment/export/laydaysstatement -o data/shipment_laydaysstatement.csv
curl datamanagement.tmc.nickelasia.com/shipment/export/laydaysdetail -o data/shipment_laydaysdetail.csv
curl datamanagement.tmc.nickelasia.com/shipment/export/trip -o data/shipment_trip.csv
curl datamanagement.tmc.nickelasia.com/shipment/export/tripdetail -o data/shipment_tripdetail.csv
