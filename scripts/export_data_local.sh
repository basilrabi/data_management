#!/usr/bin/bash

set -a
. data_management/local.py
set +a

if [ -d "data_local" ]
then
    mv data_local data_local_$(date +"%Y-%m-%d_%H-%M-%S")
fi
mkdir data_local

ogr2ogr -progress -f "GPKG" data_local/inventory_block.gpkg \
    "PG:host=$db_host user=$db_user dbname=$db_name" \
    -select name,z,ni,fe,co,excavated,geom \
    inventory_block

ogr2ogr -progress -f "GPKG" data_local/location_mineblock.gpkg \
    "PG:host=$db_host user=$db_user dbname=$db_name" \
    location_mineblock

ogr2ogr -progress -f "GPKG" data_local/location_roadarea.gpkg \
    "PG:host=$db_host user=$db_user dbname=$db_name" \
    location_roadarea

curl http://127.0.0.1:8000/custom/export/group-permissions -o data_local/group_permission.csv
curl http://127.0.0.1:8000/custom/export/groups -o data_local/groups.csv
curl http://127.0.0.1:8000/custom/export/user-groups -o data_local/user_group.csv
curl http://127.0.0.1:8000/custom/export/user-permissions -o data_local/user_permission.csv
curl http://127.0.0.1:8000/custom/export/users -o data_local/users.csv
curl http://127.0.0.1:8000/inventory/export/clustered-block -o data_local/inventory_clustered_block.csv
curl http://127.0.0.1:8000/location/export/cluster -o data_local/location_cluster.csv
curl http://127.0.0.1:8000/shipment/export/lct -o data_local/shipment_lct.csv
curl http://127.0.0.1:8000/shipment/export/lctcontract -o data_local/shipment_lctcontract.csv
curl http://127.0.0.1:8000/shipment/export/laydaysdetail -o data_local/shipment_laydaysdetail.csv
curl http://127.0.0.1:8000/shipment/export/laydaysstatement -o data_local/shipment_laydaysstatement.csv
curl http://127.0.0.1:8000/shipment/export/shipment -o data_local/shipment_shipment.csv
curl http://127.0.0.1:8000/shipment/export/trip -o data_local/shipment_trip.csv
curl http://127.0.0.1:8000/shipment/export/tripdetail -o data_local/shipment_tripdetail.csv
curl http://127.0.0.1:8000/shipment/export/vessel -o data_local/shipment_vessel.csv
