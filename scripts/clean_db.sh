#!/usr/bin/bash

source $HOME/.virtualenvs/data_management/bin/activate

set -a
. data_management/local.py
set +a

template=data_management_template

psql -h $db_host -p $db_port -U $db_user -w postgres -c "drop database if exists $db_name"

# The database data_management_template must exist in $db_host. This database
# is empty, has the extension postgis_sfcgal enabled and is owned by $db_user.
# An sql dump of the template is shown in
# scripts/sql/data_management_template.pgsql
psql -h $db_host -p $db_port -U $db_user -w postgres -c "create database $db_name template $template"

# Set-up django database
./manage.py migrate
