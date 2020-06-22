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

upload_orm () {
    echo "Running $1 script." 2>&1 | tee -a log_upload_data && \
    time_start=$(date +%s) && \
    python3 manage.py shell < scripts/upload_data/$1.py 2>&1 | tee -a log_upload_data && \
    time_end=$(date +%s) && \
    time_elapsed=$(($time_end - $time_start)) && \
    echo "orm $1, $time_elapsed" >> log_upload_data_time.csv
}

sql_script () {
    echo "Running $1/$2 script." 2>&1 | tee -a log_upload_data && \
    time_start=$(date +%s) && \
    psql -h $db_host -p $db_port -U $db_user -w $db_name -a -f scripts/sql/$1/$2.pgsql 2>&1 | tee -a log_upload_data && \
    time_end=$(date +%s) && \
    time_elapsed=$(($time_end - $time_start)) && \
    echo "sql $1-$2, $time_elapsed" >> log_upload_data_time.csv
}

vacuum () {
    echo "Running vacuum analyze on $1." 2>&1 | tee -a log_upload_data && \
    time_start=$(date +%s) && \
    psql -h $db_host -p $db_port -U $db_user -w $db_name -a -c "VACUUM ANALYZE $1" 2>&1 | tee -a log_upload_data && \
    time_end=$(date +%s) && \
    time_elapsed=$(($time_end - $time_start)) && \
    echo "vacuum $1, $time_elapsed" >> log_upload_data_time.csv
}

sql_script "upload_data" "inventory_block" && \
upload_ogr location_mineblock identity && \
upload_ogr location_roadarea identity && \
sql_script "upload_data" "location_cluster" && \
vacuum "inventory_block" && \
vacuum "location_cluster" && \
sql_script "upload_data" "inventory_clustered_block" && \
upload_orm shipment_lct && \
vacuum "shipment_lct" && \
upload_orm shipment_lctcontract && \
upload_orm shipment_vessel && \
upload_orm shipment_shipment && \
vacuum "shipment_shipment" && \
upload_orm shipment_laydaysstatement && \
vacuum "shipment_laydaysstatement" && \
sql_script "upload_data" "shipment_laydaysdetail" && \
vacuum "shipment_laydaysdetail" && \
sql_script "upload_data" "shipment_trip" && \
vacuum "shipment_trip" && \
sql_script "upload_data" "shipment_tripdetail" && \
vacuum "shipment_tripdetail" && \
upload_orm groups && \
upload_orm users && \
sql_script "function" "get_ore_class" && \
sql_script "function" "insert_dummy_cluster" && \
sql_script "trigger" "location_cluster_update" && \
sql_script "trigger" "location_drillhole_update" && \
upload_orm location_cluster_snap && \
sql_script "upload_data" "location_drillhole" && \
sql_script "upload_data" "sampling_drillcoresample" && \
sql_script "lock" "location_cluster" && \
echo "Setting up QGIS users'..." 2>&1 | tee -a log_upload_data && \
psql -h $db_host -p $db_port -U tmcgis -w postgres -c "create user geology with encrypted password '$DATA_MANAGEMENT_GEOLOGY'" 2>&1 | tee -a log_upload_data && \
psql -h $db_host -p $db_port -U tmcgis -w postgres -c "create user gradecontrol with encrypted password '$DATA_MANAGEMENT_GRADECONTROL'" 2>&1 | tee -a log_upload_data && \
psql -h $db_host -p $db_port -U tmcgis -w postgres -c "create user survey with encrypted password '$DATA_MANAGEMENT_SURVEY'" 2>&1 | tee -a log_upload_data && \
sql_script "permission" "all"
sql_script "helper" "excavate_inventory_block"
