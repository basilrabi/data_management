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

if [ "$db_name" = "data_management" ] && [ "$db_user" = "data_management" ]; then
    echo "Uploading in production." 2>&1 | tee -a log_upload_data
    extra=""
else
    echo "Uploading in test environment" 2>&1 | tee -a log_upload_data
    extra="subset"
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

sql_script "function" "array_from_geom" && \
sql_script "function" "get_ore_class" && \
sql_script "function" "gradient" && \
sql_script "function" "shipment_name_html" && \
sql_script "function" "slope_angle" && \
sql_script "function" "vectors" && \
sql_script "procedure" "insert_dummy_cluster" && \
sql_script "procedure" "record_log" && \
sql_script "upload_data" "comptrollership_activitycategory" && \
vacuum "comptrollership_activitycategory" && \
sql_script "upload_data" "comptrollership_activitycode" && \
vacuum "comptrollership_activitycode" && \
sql_script "upload_data" "comptrollership_generalledgeraccount" && \
vacuum "comptrollership_generalledgeraccount" && \
sql_script "upload_data" "comptrollership_material" && \
vacuum "comptrollership_material" && \
sql_script "upload_data" "comptrollership_costcenter" && \
vacuum "comptrollership_costcenter" && \
sql_script "upload_data" "comptrollership_operationhead" && \
vacuum "comptrollership_operationhead" && \
sql_script "upload_data" "comptrollership_profitcenter" && \
vacuum "comptrollership_profitcenter" && \
sql_script "upload_data" "comptrollership_sapcostcenter" && \
vacuum "comptrollership_sapcostcenter" && \
sql_script "upload_data" "comptrollership_monthlycost" && \
vacuum "comptrollership_monthlycost" && \
sql_script "upload_data" "custom_unitofmeasure" && \
vacuum "custom_unitofmeasure" && \
sql_script "upload_data" "fleet_capacity" && \
vacuum "fleet_capacity" && \
sql_script "upload_data" "fleet_chassisserialnumber" && \
vacuum "fleet_chassisserialnumber" && \
sql_script "upload_data" "fleet_engineserialnumber" && \
vacuum "fleet_engineserialnumber" && \
sql_script "upload_data" "fleet_equipmentclass" && \
vacuum "fleet_equipmentclass" && \
sql_script "upload_data" "fleet_equipmentmanufacturer" && \
vacuum "fleet_equipmentmanufacturer" && \
sql_script "upload_data" "fleet_platenumber" && \
vacuum "fleet_platenumber" && \
sql_script "upload_data" "mine_planning_maptype" && \
vacuum "mine_planning_maptype" && \
sql_script "upload_data" "mine_planning_mineplanningengineer" && \
vacuum "mine_planning_mineplanningengineer" && \
sql_script "upload_data" "organization_organization" && \
vacuum "organization_organization" && \
sql_script "upload_data" "organization_division" && \
vacuum "organization_division" && \
sql_script "upload_data" "organization_department" && \
vacuum "organization_department" && \
sql_script "upload_data" "organization_manilagpsapikey" && \
vacuum "organization_manilagpsapikey" && \
sql_script "upload_data" "organization_section" && \
vacuum "organization_section" && \
sql_script "helper" "organization_organizationunit" && \
vacuum "organization_organizationunit" && \
sql_script "upload_data" "billing_billingtracker" && \
sql_script "upload_data" "billing_billingtracker_id_seq" && \
vacuum "billing_billingaddon" && \
vacuum "billing_billingtracker" && \
sql_script "upload_data" "billing_cmbilling" && \
vacuum "billing_cmbilling" && \
sql_script "upload_data" "inventory_block$extra" && \
upload_ogr location_blgu identity && \
upload_ogr location_fla identity && \
upload_ogr location_mineblock identity && \
upload_ogr location_mpsa identity && \
upload_ogr location_peza identity && \
upload_ogr location_roadarea identity && \
upload_ogr location_slice identity && \
sql_script "trigger" "location_cluster_insert" && \
sql_script "upload_data" "comptrollership_costcenterconversion" && \
vacuum "comptrollership_costcenterconversion" && \
sql_script "upload_data" "comptrollership_costcenterconversion_equipment" && \
vacuum "comptrollership_costcenterconversion_equipment" && \
sql_script "upload_data" "fleet_bodytype" && \
vacuum "fleet_bodytype" && \
sql_script "upload_data" "fleet_equipmentmodel" && \
vacuum "fleet_equipmentmodel" && \
sql_script "upload_data" "fleet_equipment" && \
vacuum "fleet_equipment" && \
sql_script "upload_data" "fleet_equipmentidlingtime" && \
vacuum "fleet_equipmentidlingtime" && \
sql_script "select" "fleet_equipmentidlinginterval" && \
sql_script "index" "fleet_equipmentidlinginterval" && \
vacuum "fleet_equipmentidlinginterval" && \
sql_script "upload_data" "fleet_equipmentignitionstatus" && \
vacuum "fleet_equipmentignitionstatus" && \
sql_script "select" "fleet_equipmentignitioninterval" && \
sql_script "index" "fleet_equipmentignitioninterval" && \
vacuum "fleet_equipmentignitioninterval" && \
sql_script "upload_data" "fleet_additionalequipmentcost" && \
vacuum "fleet_additionalequipmentcost" && \
sql_script "upload_data" "fleet_equipmentmobilenumber" && \
vacuum "fleet_equipmentmobilenumber" && \
sql_script "upload_data" "fleet_providerequipmentregistry" && \
vacuum "fleet_providerequipmentregistry" && \
sql_script "upload_data" "fleet_providerequipmentrequirement" && \
vacuum "fleet_providerequipmentrequirement" && \
sql_script "upload_data" "fleet_providerequipmentrequirementdetail" && \
vacuum "fleet_providerequipmentrequirementdetail" && \
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
sql_script "upload_data" "mine_planning_mapdocumentcontrol" && \
vacuum "mine_planning_mapdocumentcontrol" && \
sql_script "upload_data" "ormm_externalincomingcommunication" && \
vacuum "ormm_externalincomingcommunication" && \
sql_script "upload_data" "ormm_externalcommunication" && \
vacuum "ormm_externalcommunication" && \
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
sql_script "upload_data" "shipment_draftsurvey" && \
vacuum "shipment_draftsurvey" && \
sql_script "upload_data" "shipment_laydaysstatement" && \
vacuum "shipment_laydaysstatement" && \
sql_script "upload_data" "billing_shipmentbilling" && \
vacuum "billing_shipmentbilling" && \
sql_script "upload_data" "billing_shipmentbillingentry" && \
vacuum "billing_shipmentbillingentry" && \
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
sql_script "upload_data" "location_equipmentlocation$extra" && \
vacuum "location_equipmentlocation" && \
sql_script "select" "location_haulingequipment" && \
sql_script "index" "location_haulingequipment" && \
vacuum "location_haulingequipment" && \
sql_script "select" "location_haulingequipmentpath" && \
sql_script "index" "location_haulingequipmentpath" && \
vacuum "location_haulingequipmentpath" && \
sql_script "select" "location_loadingequipment" && \
sql_script "index" "location_loadingequipment" && \
vacuum "location_loadingequipment" && \
sql_script "select" "location_loadingequipmentpath" && \
sql_script "index" "location_loadingequipmentpath" && \
vacuum "location_loadingequipmentpath" && \
sql_script "upload_data" "sampling_shipmentloadingassay" && \
vacuum "sampling_shipmentloadingassay" && \
sql_script "upload_data" "sampling_shipmentloadinglotassay" && \
vacuum "sampling_shipmentloadinglotassay" && \
sql_script "upload_data" "sampling_approvedshipmentloadingassay" && \
vacuum "sampling_approvedshipmentloadingassay" && \
sql_script "select" "dash_equipmentusage" && \
sql_script "index" "dash_equipmentusage" && \
vacuum "dash_equipmentusage" && \
sql_script "trigger" "inventory_block_exposed" && \
sql_script "trigger" "location_anchorage_update" && \
sql_script "trigger" "location_clippedcluster_insert" && \
sql_script "trigger" "location_clippedcluster_update" && \
sql_script "trigger" "location_cluster_update" && \
sql_script "trigger" "location_clusterlayout" && \
sql_script "trigger" "location_crest_insert" && \
sql_script "trigger" "location_crest_update" && \
sql_script "trigger" "location_drillhole_update" && \
sql_script "trigger" "organization_organizationunit_delete" && \
sql_script "trigger" "organization_organizationunit_insert" && \
sql_script "trigger" "organization_organizationunit_update" && \
sql_script "trigger" "shipment_trip_update" && \
psql -h $db_host -p $db_port -U $db_user -w $db_name -c "call insert_dummy_cluster()"
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
