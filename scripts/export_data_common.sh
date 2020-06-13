
if [ -d "$datadir" ]
then
    mv "$datadir" "$datadir"_$(date +"%Y-%m-%d_%H-%M-%S")
fi
mkdir $datadir

download_sql () {
    sql=$(cat scripts/sql/select/$1.pgsql | tr "[[:space:]]+" " " | tr -s " ") && \
    cmd="\COPY ($sql) TO '$(pwd)/$datadir/$1.csv' WITH CSV" && \
    psql -h $db_host -U $db_user $db_name -c "$cmd"
}

echo "Exporting location_mineblock..." && \
ogr2ogr -progress -f "GPKG" $datadir/location_mineblock.gpkg \
    "PG:host=$db_host user=$db_user dbname=$db_name" \
    location_mineblock && \
echo "Exporting location_roadarea..." && \
ogr2ogr -progress -f "GPKG" $datadir/location_roadarea.gpkg \
    "PG:host=$db_host user=$db_user dbname=$db_name" \
    location_roadarea && \
echo "Exporting inventory_block..." && \
download_sql inventory_block && \
echo "Exporting sampling_drillcoresample..." && \
download_sql sampling_drillcoresample && \
echo "Exporting group_permission..." && \
curl $address/custom/export/group-permissions -o $datadir/group_permission.csv && \
echo "Exporting groups..." && \
curl $address/custom/export/groups -o $datadir/groups.csv && \
echo "Exporting user_group..." && \
curl $address/custom/export/user-groups -o $datadir/user_group.csv && \
echo "Exporting user_permissions..." && \
curl $address/custom/export/user-permissions -o $datadir/user_permission.csv && \
echo "Exporting users..." && \
curl $address/custom/export/users -o $datadir/users.csv && \
echo "Exporting clustered_block..." && \
curl $address/inventory/export/clustered-block -o $datadir/inventory_clustered_block.csv && \
echo "Exporting cluster..." && \
curl $address/location/export/cluster -o $datadir/location_cluster.csv && \
echo "Exporting location_drillhole..." && \
curl $address/location/export/drillhole -o $datadir/location_drillhole.csv && \
echo "Exporting shipment_lct..." && \
curl $address/shipment/export/lct -o $datadir/shipment_lct.csv && \
echo "Exporting shipment_lctcontract..." && \
curl $address/shipment/export/lctcontract -o $datadir/shipment_lctcontract.csv && \
echo "Exporting shipment_laydaysdetail..." && \
download_sql shipment_laydaysdetail && \
echo "Exporting shipment_laydaysstatement..." && \
curl $address/shipment/export/laydaysstatement -o $datadir/shipment_laydaysstatement.csv && \
echo "Exporting shipment_shipment..." && \
curl $address/shipment/export/shipment -o $datadir/shipment_shipment.csv && \
echo "Exporting shipment_trip..." && \
curl $address/shipment/export/trip -o $datadir/shipment_trip.csv && \
echo "Exporting shipment_tripdetail..." && \
curl $address/shipment/export/tripdetail -o $datadir/shipment_tripdetail.csv && \
echo "Exporting shipment_vessel..." && \
curl $address/shipment/export/vessel -o $datadir/shipment_vessel.csv
