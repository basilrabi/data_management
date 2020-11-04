#!/usr/bin/bash

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

sql_script "upload_data" "inventory_block" && \
upload_ogr location_fla identity && \
upload_ogr location_mineblock identity && \
upload_ogr location_mpsa identity && \
upload_ogr location_peza identity && \
upload_ogr location_roadarea identity && \
upload_ogr location_slice identity && \
sql_script "trigger" "location_cluster_insert" && \
sql_script "upload_data" "location_cluster" && \
vacuum "inventory_block" && \
vacuum "location_cluster" && \
sql_script "upload_data" "inventory_clustered_block" && \
vacuum "inventory_block" && \
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
sql_script "upload_data" "shipment_laydaysdetail" && \
vacuum "shipment_laydaysdetail" && \
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
upload_orm groups && \
upload_orm users && \
sql_script "upload_data" "sampling_shipmentloadingassay" && \
vacuum "sampling_shipmentloadingassay" && \
sql_script "upload_data" "sampling_shipmentloadinglotassay" && \
vacuum "sampling_shipmentloadinglotassay" && \
sql_script "upload_data" "sampling_approvedshipmentloadingassay" && \
vacuum "sampling_approvedshipmentloadingassay" && \
sql_script "function" "get_ore_class" && \
sql_script "function" "shipment_name_html" && \
sql_script "function" "insert_dummy_cluster" && \
sql_script "trigger" "inventory_block_exposed" && \
sql_script "trigger" "location_cluster_update" && \
sql_script "trigger" "location_drillhole_update" && \
psql -h $db_host -p $db_port -U $db_user -w $db_name -c "select insert_dummy_cluster()"
sql_script "upload_data" "location_drillhole" && \
sql_script "upload_data" "sampling_drillcoresample" && \
sql_script "lock" "location_cluster" && \
echo "Setting up QGIS users'..." 2>&1 | tee -a log_upload_data && \
psql -h $db_host -p $db_port -U tmcgis -w postgres -c "create user geology      with inherit encrypted password '$DATA_MANAGEMENT_GEOLOGY'"      2>&1 | tee -a log_upload_data && \
psql -h $db_host -p $db_port -U tmcgis -w postgres -c "create user gradecontrol with inherit encrypted password '$DATA_MANAGEMENT_GRADECONTROL'" 2>&1 | tee -a log_upload_data && \
psql -h $db_host -p $db_port -U tmcgis -w postgres -c "create user planning     with inherit encrypted password '$DATA_MANAGEMENT_PLANNING'"     2>&1 | tee -a log_upload_data && \
psql -h $db_host -p $db_port -U tmcgis -w postgres -c "create user reader       with inherit encrypted password '$DATA_MANAGEMENT_READER'"       2>&1 | tee -a log_upload_data && \
psql -h $db_host -p $db_port -U tmcgis -w postgres -c "create user survey       with inherit encrypted password '$DATA_MANAGEMENT_SURVEY'"       2>&1 | tee -a log_upload_data && \
sql_script "permission" "all"
sql_script "helper" "excavate_inventory_block"
sql_script "helper" "excavate_sampling_drillcoresample"
sql_script "helper" "update_location_drillhole_z_present"
