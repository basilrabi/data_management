
if [ -d "$datadir" ]
then
    mv "$datadir" "$datadir"_$(date +"%Y-%m-%d_%H-%M-%S")
fi
mkdir $datadir

download_ogr () {
    echo "Exporting $1..." && \
    ogr2ogr -progress -f "GPKG" $datadir/$1.gpkg "PG:host=$db_host user=$db_user dbname=$db_name" $1
}

download_sql () {
    echo "Exporting $1..." && \
    sql=$(cat scripts/sql/select/$1.pgsql | tr "[[:space:]]+" " " | tr -s " ") && \
    cmd="\COPY ($sql) TO '$(pwd)/$datadir/$1.csv' WITH CSV" && \
    psql -h $db_host -U $db_user $db_name -c "$cmd"
}

download_ogr location_mineblock && \
download_ogr location_roadarea && \
download_ogr location_slice && \
download_sql inventory_block && \
download_sql inventory_clustered_block && \
download_sql location_cluster && \
download_sql location_drillhole && \
download_sql sampling_drillcoresample && \
download_sql sampling_laboratory && \
download_sql sampling_shipmentdischargeassay && \
download_sql sampling_shipmentdischargelotassay && \
download_sql sampling_shipmentloadingassay && \
download_sql sampling_shipmentloadinglotassay && \
download_sql shipment_buyer && \
download_sql shipment_destination && \
download_sql shipment_laydaysdetail && \
download_sql shipment_laydaysstatement && \
download_sql shipment_lct && \
download_sql shipment_lctcontract && \
download_sql shipment_product && \
download_sql shipment_shipment && \
download_sql shipment_trip && \
download_sql shipment_tripdetail && \
download_sql shipment_vessel && \
echo "Exporting group_permission..." && \
curl $address/custom/export/group-permissions -o $datadir/group_permission.csv && \
echo "Exporting groups..." && \
curl $address/custom/export/groups -o $datadir/groups.csv && \
echo "Exporting user_group..." && \
curl $address/custom/export/user-groups -o $datadir/user_group.csv && \
echo "Exporting user_permissions..." && \
curl $address/custom/export/user-permissions -o $datadir/user_permission.csv && \
echo "Exporting users..." && \
curl $address/custom/export/users -o $datadir/users.csv
