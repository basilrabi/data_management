#!/usr/bin/bash

set -a
. data_management/local.py
set +a

psql -h $db_host -p $db_port -U $db_user -w postgres -c "drop database if exists $db_name"

# The database data_management_template must exist in $db_host. This database
# is empty, has the extension postgis_sfcgal enabled and is owned by $db_user.
# An sql dump of the template is shown in
# scripts/sql/data_management_template.pgsql
psql -h $db_host -p $db_port -U $db_user -w postgres -c "create database $db_name template data_management_template"

# Set-up django database
./manage.py migrate
./manage.py createsuperuser --noinput

psql -h $db_host -p $db_port -U tmcgis -w $db_name -c "create schema area"

echo "Setting up qgis user 'gradecontrol'..."
psql -h $db_host -p $db_port -U tmcgis -w postgres -c "drop role if exists gradecontrol"
psql -h $db_host -p $db_port -U tmcgis -w postgres -c "create user gradecontrol with encrypted password '$DATA_MANAGEMENT_GRADECONTROL'"
psql -h $db_host -p $db_port -U tmcgis -w $db_name -c "grant select on table inventory_block to gradecontrol"
psql -h $db_host -p $db_port -U tmcgis -w $db_name -c "grant select on table location_cluster to gradecontrol"
psql -h $db_host -p $db_port -U tmcgis -w $db_name -c "grant update (excavated, cluster_id) on table inventory_block to gradecontrol"
psql -h $db_host -p $db_port -U tmcgis -w $db_name -c "grant update (excavated, distance_from_road) on table location_cluster to gradecontrol"

echo "Setting up qgis user 'survey'..."
psql -h $db_host -p $db_port -U tmcgis -w postgres -c "drop role if exists survey"
psql -h $db_host -p $db_port -U tmcgis -w postgres -c "create user survey with encrypted password '$DATA_MANAGEMENT_SURVEY'"
psql -h $db_host -p $db_port -U tmcgis -w $db_name -c "grant select on table location_cluster to survey"
psql -h $db_host -p $db_port -U tmcgis -w $db_name -c "grant update (with_layout) on table location_cluster to survey"
