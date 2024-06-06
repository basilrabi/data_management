#!/usr/bin/bash

source $HOME/.virtualenvs/data_management/bin/activate

set -a
. data_management/local.py
set +a


psql -h $db_host -p $db_port -U $db_user -w postgres -c "drop database if exists $db_name"

# The database $db_template must exist in $db_host.
# This database is empty, has the extensions pg_trgm, pgrouting, and postgis_sfcgal enabled and is owned by $db_user.
psql -h $db_host -p $db_port -U $db_user -w postgres -c "create database $db_name template $db_template"

# Set-up django database
./manage.py migrate

