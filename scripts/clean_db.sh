#!/usr/bin/bash

set -a
. data_management/local.py
set +a

psql -h $db_host -p $db_port -U $db_user -w postgres -c "drop database if exists $db_name"

# The database data_management_template must exist in $db_host. This database
# is empty, has the extension postgis_sfcgal enabled and is owned by $db_user.
psql -h $db_host -p $db_port -U $db_user -w postgres -c "create database $db_name template data_management_template"

# Set-up django database
./manage.py migrate
./manage.py createsuperuser --noinput

# Set-up permission for qgis user `gradecontrol`
psql -h $db_host -p $db_port -U tmcgis -w postgres -c "drop role if exists gradecontrol"
psql -h $db_host -p $db_port -U tmcgis -w postgres -c "create role gradecontrol password '$DATA_MANAGEMENT_GRADECONTROL'"
psql -h $db_host -p $db_port -U tmcgis -w postgres -c "alter role gradecontrol login"
psql -h $db_host -p $db_port -U tmcgis -w $db_name -c "grant select on table inventory_block to gradecontrol"
psql -h $db_host -p $db_port -U tmcgis -w $db_name -c "grant update (excavated, cluster_id) on table inventory_block to gradecontrol"
