
if [ -d "$datadir" ]
then
    mv "$datadir" "$datadir"_$(date +"%Y-%m-%d_%H-%M-%S")
fi
mkdir $datadir
ls -1 | grep -P "^${datadir}_\d{4}-\d{2}" | sort -r | tail -n +4 | xargs -d '\n' rm -r

download_ogr () {
    echo "Exporting $1..." && \
    ogr2ogr -progress -f "GPKG" $datadir/$1.gpkg "PG:host=$db_host user=$db_user dbname=$db_name" $1
}

download_sql () {
    echo "Exporting $1..." && \
    sql=$(cat scripts/sql/select/$1.pgsql | tr "[:space:]" " " | tr -s " ") && \
    cmd="\COPY ($sql) TO '$(pwd)/$datadir/$1.csv' WITH CSV" && \
    psql -h $db_host -U $db_user $db_name -c "$cmd"
}

download_ogr location_fla && \
download_ogr location_mineblock && \
download_ogr location_mpsa && \
download_ogr location_peza && \
download_ogr location_roadarea && \
download_ogr location_slice && \
download_sql billing_billingaddon && \
download_sql billing_billingtracker && \
download_sql comptrollership_costcenter && \
download_sql comptrollership_costcenterconversion && \
download_sql comptrollership_generalledgeraccount && \
download_sql comptrollership_sapcostcenter && \
download_sql custom_profession && \
download_sql custom_professionalidentificationcard && \
download_sql custom_mobilenumber && \
download_sql fleet_equipment && \
download_sql fleet_equipmentclass && \
download_sql fleet_equipmentmanufacturer && \
download_sql fleet_equipmentmodel && \
download_sql inventory_block && \
download_sql inventory_clustered_block && \
download_sql local_calendar_holiday && \
download_sql local_calendar_holidayevent && \
download_sql location_anchorage && \
download_sql location_cluster && \
download_sql location_clusterlayout && \
download_sql location_drillhole && \
download_sql location_equipmentlocation && \
download_sql material_management_legacygoodsissuance && \
download_sql material_management_legacygoodsreceivednote && \
download_sql material_management_legacyitemtype && \
download_sql material_management_legacymaterial && \
download_sql material_management_legacyvendor && \
download_sql material_management_material && \
download_sql material_management_materialgroup && \
download_sql material_management_materialtype && \
download_sql material_management_unitofmeasure && \
download_sql material_management_valuation && \
download_sql organization_department && \
download_sql organization_division && \
download_sql organization_organization && \
download_sql organization_section && \
download_sql sampling_approvedshipmentdischargeassay && \
download_sql sampling_approvedshipmentloadingassay && \
download_sql sampling_drillcoresample && \
download_sql sampling_laboratory && \
download_sql sampling_lithology && \
download_sql sampling_shipmentdischargeassay && \
download_sql sampling_shipmentdischargelotassay && \
download_sql sampling_shipmentloadingassay && \
download_sql sampling_shipmentloadinglotassay && \
download_sql shipment_approvedlaydaysstatement && \
download_sql shipment_buyer && \
download_sql shipment_destination && \
download_sql shipment_laydaysdetail && \
download_sql shipment_laydaysdetailcomputed && \
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
./scripts/R/export_external_data.R
