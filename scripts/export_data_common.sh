
if [ -d "$datadir" ]
then
    mv "$datadir" "$datadir"_$(date +"%Y-%m-%d_%H-%M-%S")
fi
mkdir $datadir

ogr2ogr -progress -f "GPKG" $datadir/inventory_block.gpkg \
    "PG:host=$db_host user=$db_user dbname=$db_name" \
    -select name,z,ni,fe,co,excavated,geom \
    inventory_block

ogr2ogr -progress -f "GPKG" $datadir/location_mineblock.gpkg \
    "PG:host=$db_host user=$db_user dbname=$db_name" \
    location_mineblock

ogr2ogr -progress -f "GPKG" $datadir/location_roadarea.gpkg \
    "PG:host=$db_host user=$db_user dbname=$db_name" \
    location_roadarea

curl $address/custom/export/group-permissions -o $datadir/group_permission.csv
curl $address/custom/export/groups -o $datadir/groups.csv
curl $address/custom/export/user-groups -o $datadir/user_group.csv
curl $address/custom/export/user-permissions -o $datadir/user_permission.csv
curl $address/custom/export/users -o $datadir/users.csv
curl $address/inventory/export/clustered-block -o $datadir/inventory_clustered_block.csv
curl $address/location/export/cluster -o $datadir/location_cluster.csv
curl $address/shipment/export/lct -o $datadir/shipment_lct.csv
curl $address/shipment/export/lctcontract -o $datadir/shipment_lctcontract.csv
curl $address/shipment/export/laydaysdetail -o $datadir/shipment_laydaysdetail.csv
curl $address/shipment/export/laydaysstatement -o $datadir/shipment_laydaysstatement.csv
curl $address/shipment/export/shipment -o $datadir/shipment_shipment.csv
curl $address/shipment/export/trip -o $datadir/shipment_trip.csv
curl $address/shipment/export/tripdetail -o $datadir/shipment_tripdetail.csv
curl $address/shipment/export/vessel -o $datadir/shipment_vessel.csv
