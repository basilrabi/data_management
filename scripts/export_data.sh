#!/usr/bin/bash

if [ -d "data" ]
then
    mv data data_$(date +"%Y-%m-%d_%H-%M-%S")
fi
mkdir data

ogr2ogr -progress -f "GPKG" data/area.road.gpkg \
    "PG:host=$DATA_MANAGEMENT_DB_HOST user=$DATA_MANAGEMENT_DB_USER dbname=$DATA_MANAGEMENT_DB_NAME" \
    area.road

ogr2ogr -progress -f "GPKG" data/inventory_block.gpkg \
    "PG:host=$DATA_MANAGEMENT_DB_HOST user=$DATA_MANAGEMENT_DB_USER dbname=$DATA_MANAGEMENT_DB_NAME" \
    -select name,z,ni,fe,co,excavated,geom \
    inventory_block

ogr2ogr -progress -f "GPKG" data/location_mineblock.gpkg \
    "PG:host=$DATA_MANAGEMENT_DB_HOST user=$DATA_MANAGEMENT_DB_USER dbname=$DATA_MANAGEMENT_DB_NAME" \
    location_mineblock

curl datamanagement.tmc.nickelasia.com/custom/export/group-permissions -o data/group_permission.csv
curl datamanagement.tmc.nickelasia.com/custom/export/groups -o data/groups.csv
curl datamanagement.tmc.nickelasia.com/custom/export/user-groups -o data/user_group.csv
curl datamanagement.tmc.nickelasia.com/custom/export/user-permissions -o data/user_permission.csv
curl datamanagement.tmc.nickelasia.com/custom/export/users -o data/users.csv
curl datamanagement.tmc.nickelasia.com/inventory/export/clustered-block -o data/inventory_clustered_block.csv
curl datamanagement.tmc.nickelasia.com/location/export/cluster -o data/location_cluster.csv
curl datamanagement.tmc.nickelasia.com/shipment/export/lct -o data/shipment_lct.csv
curl datamanagement.tmc.nickelasia.com/shipment/export/lctcontract -o data/shipment_lctcontract.csv
curl datamanagement.tmc.nickelasia.com/shipment/export/laydaysdetail -o data/shipment_laydaysdetail.csv
curl datamanagement.tmc.nickelasia.com/shipment/export/laydaysstatement -o data/shipment_laydaysstatement.csv
curl datamanagement.tmc.nickelasia.com/shipment/export/shipment -o data/shipment_shipment.csv
curl datamanagement.tmc.nickelasia.com/shipment/export/trip -o data/shipment_trip.csv
curl datamanagement.tmc.nickelasia.com/shipment/export/tripdetail -o data/shipment_tripdetail.csv
curl datamanagement.tmc.nickelasia.com/shipment/export/vessel -o data/shipment_vessel.csv
