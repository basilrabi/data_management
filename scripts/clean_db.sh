#!/usr/bin/bash

set -a
. data_management/local.py
set +a

psql -h $db_host -U $db_user -w postgres -c "drop database if exists $db_name"
psql -h $db_host -U $db_user -w postgres -c "create database $db_name"
psql -h $db_host -U $db_user -w $db_name -c "create extension postgis"
