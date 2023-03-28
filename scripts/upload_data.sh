#!/usr/bin/bash

source $HOME/.virtualenvs/data_management/bin/activate

set -a
. data_management/local.py
set +a

if [ -f "log_upload_data" ]
then
    mv log_upload_data log_upload_data_$(date +"%Y-%m-%d_%H-%M-%S")
fi

if [ -f "log_upload_data_time.csv" ]
then
    mv log_upload_data_time.csv log_upload_data_time_$(date +"%Y-%m-%d_%H-%M-%S").csv
fi

source scripts/functions.sh

upload_ogr () {
    echo "Uploading $1." 2>&1 | tee -a log_upload_data && \
    time_start=$(date +%s) && \
    ogr2ogr -update -append -progress \
        -f PostgreSQL "PG:host=$db_host port=$db_port user=$db_user dbname=$db_name password=$db_password" \
        -fieldmap "$2" \
        -nln $1 data/$1.gpkg 2>&1 | tee -a log_upload_data && \
    time_end=$(date +%s) && \
    time_elapsed=$(($time_end - $time_start)) && \
    echo "ogr $1, $time_elapsed" >> log_upload_data_time.csv
}

sql_script "function" "array_from_geom" && \
sql_script "function" "get_ore_class" && \
sql_script "function" "gradient" && \
sql_script "function" "shipment_name_html" && \
sql_script "function" "slope_angle" && \
sql_script "function" "vectors" && \
sql_script "procedure" "insert_dummy_cluster" && \
sql_script "procedure" "record_log" && \
sql_script "upload_data" "comptrollership_costcenter" && \
vacuum "comptrollership_costcenter" && \
sql_script "upload_data" "comptrollership_generalledgeraccount" && \
vacuum "comptrollership_generalledgeraccount" && \
sql_script "upload_data" "comptrollership_sapcostcenter" && \
vacuum "comptrollership_sapcostcenter" && \
sql_script "upload_data" "comptrollership_costcenterconversion" && \
vacuum "comptrollership_costcenterconversion" && \
sql_script "upload_data" "fleet_equipmentclass" && \
vacuum "fleet_equipmentclass" && \
sql_script "upload_data" "fleet_equipmentmanufacturer" && \
vacuum "fleet_equipmentmanufacturer" && \
sql_script "upload_data" "organization_organization" && \
vacuum "organization_organization" && \
sql_script "upload_data" "billing_billingtracker" && \
sql_script "upload_data" "billing_billingtracker_id_seq" && \
vacuum "billing_billingaddon" && \
vacuum "billing_billingtracker" && \
sql_script "upload_data" "inventory_block" && \
upload_ogr location_fla identity && \
upload_ogr location_mineblock identity && \
upload_ogr location_mpsa identity && \
upload_ogr location_peza identity && \
upload_ogr location_roadarea identity && \
upload_ogr location_slice identity && \
sql_script "trigger" "location_cluster_insert" && \
sql_script "upload_data" "fleet_equipmentmodel" && \
vacuum "fleet_equipmentmodel" && \
sql_script "upload_data" "fleet_equipment" && \
vacuum "fleet_equipment" && \
sql_script "upload_data" "local_calendar_holidayevent" && \
vacuum "local_calendar_holidayevent" && \
sql_script "upload_data" "local_calendar_holiday" && \
vacuum "local_calendar_holiday" && \
sql_script "upload_data" "location_cluster" && \
sql_script "upload_data" "location_clusterlayout" && \
vacuum "inventory_block" && \
vacuum "location_cluster" && \
vacuum "location_clusterlayout" && \
sql_script "upload_data" "inventory_clustered_block" && \
vacuum "inventory_block" && \
sql_script "upload_data" "compute_location_cluster_excavation_rate" && \
sql_script "upload_data" "compute_location_cluster_latest_layout_date" && \
sql_script "upload_data" "location_crest" && \
vacuum "location_crest" && \
sql_script "upload_data" "location_clippedcluster" && \
vacuum "location_clippedcluster" && \
sql_script "upload_data" "material_management_legacyitemtype" && \
vacuum "material_management_legacyitemtype" && \
sql_script "upload_data" "material_management_legacyvendor" && \
vacuum "material_management_legacyvendor" && \
sql_script "upload_data" "material_management_legacymaterial" && \
vacuum "material_management_legacymaterial" && \
sql_script "upload_data" "material_management_legacygoodsissuance" && \
vacuum "material_management_legacygoodsissuance" && \
sql_script "upload_data" "material_management_legacygoodsreceivednote" && \
vacuum "material_management_legacygoodsreceivednote" && \
sql_script "upload_data" "material_management_materialgroup" && \
vacuum "material_management_materialgroup" && \
sql_script "upload_data" "material_management_materialtype" && \
vacuum "material_management_materialtype" && \
sql_script "upload_data" "material_management_unitofmeasure" && \
vacuum "material_management_unitofmeasure" && \
sql_script "upload_data" "material_management_valuation" && \
vacuum "material_management_valuation" && \
sql_script "upload_data" "material_management_material" && \
vacuum "material_management_material" && \
sql_script "upload_data" "sampling_laboratory" && \
vacuum "sampling_laboratory" && \
sql_script "upload_data" "sampling_lithology" && \
vacuum "sampling_lithology" && \
sql_script "upload_data" "shipment_buyer" && \
vacuum "shipment_buyer" && \
sql_script "upload_data" "shipment_destination" && \
vacuum "shipment_destination" && \
sql_script "upload_data" "shipment_product" && \
vacuum "shipment_product" && \
sql_script "upload_data" "shipment_lct" && \
vacuum "shipment_lct" && \
sql_script "upload_data" "shipment_lctcontract" && \
vacuum "shipment_lctcontract" && \
sql_script "upload_data" "shipment_vessel" && \
vacuum "shipment_vessel" && \
sql_script "upload_data" "shipment_shipment" && \
vacuum "shipment_shipment" && \
sql_script "upload_data" "shipment_laydaysstatement" && \
vacuum "shipment_laydaysstatement" && \
sql_script "upload_data" "location_anchorage" && \
vacuum "location_anchorage" && \
sql_script "upload_data" "shipment_laydaysdetail" && \
vacuum "shipment_laydaysdetail" && \
sql_script "upload_data" "shipment_laydaysdetailcomputed" && \
vacuum "shipment_laydaysdetailcomputed" && \
sql_script "upload_data" "shipment_approvedlaydaysstatement" && \
vacuum "shipment_approvedlaydaysstatement" && \
sql_script "upload_data" "shipment_trip" && \
vacuum "shipment_trip" && \
sql_script "upload_data" "shipment_tripdetail" && \
vacuum "shipment_tripdetail" && \
sql_script "select" "shipment_loadingrate" && \
sql_script "index" "shipment_loadingrate" && \
sql_script "select" "shipment_number" && \
sql_script "index" "shipment_number" && \
sql_script "upload_data" "sampling_shipmentdischargeassay" && \
vacuum "sampling_shipmentdischargeassay" && \
sql_script "upload_data" "sampling_shipmentdischargelotassay" && \
vacuum "sampling_shipmentdischargelotassay" && \
sql_script "upload_data" "sampling_approvedshipmentdischargeassay" && \
vacuum "sampling_approvedshipmentdischargeassay" && \
sql_script "upload_data" "custom_profession" && \
vacuum "custom_profession" && \
upload_orm groups && \
upload_orm users && \
sql_script "upload_data" "custom_mobilenumber" && \
vacuum "custom_mobilenumber" && \
sql_script "upload_data" "custom_professionalidentificationcard" && \
vacuum "custom_professionalidentificationcard" && \
sql_script "upload_data" "location_equipmentlocation" && \
vacuum "location_equipmentlocation" && \
sql_script "upload_data" "sampling_shipmentloadingassay" && \
vacuum "sampling_shipmentloadingassay" && \
sql_script "upload_data" "sampling_shipmentloadinglotassay" && \
vacuum "sampling_shipmentloadinglotassay" && \
sql_script "upload_data" "sampling_approvedshipmentloadingassay" && \
vacuum "sampling_approvedshipmentloadingassay" && \
sql_script "trigger" "inventory_block_exposed" && \
sql_script "trigger" "location_anchorage_update" && \
sql_script "trigger" "location_clippedcluster_insert" && \
sql_script "trigger" "location_clippedcluster_update" && \
sql_script "trigger" "location_cluster_update" && \
sql_script "trigger" "location_clusterlayout" && \
sql_script "trigger" "location_crest_insert" && \
sql_script "trigger" "location_crest_update" && \
sql_script "trigger" "location_drillhole_update" && \
sql_script "trigger" "shipment_trip_update" && \
psql -h $db_host -p $db_port -U $db_user -w $db_name -c "select insert_dummy_cluster()"
sql_script "upload_data" "location_drillhole" && \
sql_script "upload_data" "sampling_drillcoresample" && \
sql_script "constraint" "location_slice" && \
sql_script "lock" "location_cluster" && \
sql_script "lock" "location_clusterlayout" && \
sql_script "lock" "location_slice" && \
echo "Setting up QGIS users'..." 2>&1 | tee -a log_upload_data && \
psql -h $db_host -p $db_port -U $db_user -w postgres -c "create user geology      with inherit encrypted password '$DATA_MANAGEMENT_GEOLOGY'"      2>&1 | tee -a log_upload_data && \
psql -h $db_host -p $db_port -U $db_user -w postgres -c "create user gradecontrol with inherit encrypted password '$DATA_MANAGEMENT_GRADECONTROL'" 2>&1 | tee -a log_upload_data && \
psql -h $db_host -p $db_port -U $db_user -w postgres -c "create user planning     with inherit encrypted password '$DATA_MANAGEMENT_PLANNING'"     2>&1 | tee -a log_upload_data && \
psql -h $db_host -p $db_port -U $db_user -w postgres -c "create user reader       with inherit encrypted password '$DATA_MANAGEMENT_READER'"       2>&1 | tee -a log_upload_data && \
psql -h $db_host -p $db_port -U $db_user -w postgres -c "create user survey       with inherit encrypted password '$DATA_MANAGEMENT_SURVEY'"       2>&1 | tee -a log_upload_data && \
sql_script "permission" "reader"
sql_script "permission" "geology"
sql_script "permission" "gradecontrol"
sql_script "permission" "survey"
sql_script "permission" "planning"
if [ "$db_user" != "data_management" ];
then
    sed -e "s/data_management/$db_user/" scripts/sql/permission/data_management.pgsql > "scripts/sql/permission/$db_user.pgsql"
    sql_script "permission" "$db_user"
    rm "scripts/sql/permission/$db_user.pgsql"
else
    sql_script "permission" "data_management"
fi
sql_script "helper" "excavate_inventory_block"
sql_script "helper" "excavate_sampling_drillcoresample"
sql_script "helper" "gammu"
sql_script "helper" "update_location_drillhole_z_present"
./scripts/R/upload_external_data.R 2>&1 | tee -a log_upload_data
sql_script "permission" "reader-default"
sql_script "permission" "reader-default" "geology"
sql_script "permission" "reader-default" "gradecontrol"
sql_script "permission" "reader-default" "survey"
sql_script "permission" "reader-default" "planning"
