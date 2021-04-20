#!/usr/bin/bash

set -a
. data_management/local.py
set +a

template=data_management_template

if [ $# -gt 0 ]
then
    if [ $1 == light ]
    then
        echo "Using light database."
        template=data_management_template_no_topo
    else
        echo "Only accepted argument is 'light'."
        exit 1
    fi
fi

psql -h $db_host -p $db_port -U $db_user -w postgres -c "drop database if exists $db_name"
psql -h $db_host -p $db_port -U $db_user -w postgres -c "drop role if exists geology"
psql -h $db_host -p $db_port -U $db_user -w postgres -c "drop role if exists gradecontrol"
psql -h $db_host -p $db_port -U $db_user -w postgres -c "drop role if exists planning"
psql -h $db_host -p $db_port -U $db_user -w postgres -c "drop role if exists survey"

# The database data_management_template must exist in $db_host. This database
# is empty, has the extension postgis_sfcgal enabled and is owned by $db_user.
# An sql dump of the template is shown in
# scripts/sql/data_management_template.pgsql
psql -h $db_host -p $db_port -U $db_user -w postgres -c "create database $db_name template $template"

# Set-up django database
./manage.py migrate
./manage.py createsuperuser --noinput

psql -h $db_host -p $db_port -U $db_user -w $db_name -c "create schema staging"

if [ $2 == test ]
then
    echo "Testing."
else
    psql -h $db_host -p $db_port -U $db_user -w $db_name -a -f scripts/sql/constraint/location_slice.pgsql
fi
