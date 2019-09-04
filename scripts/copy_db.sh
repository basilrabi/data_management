#!/usr/bin/bash

db_cmd='-h localhost -U djangotest'

psql $db_cmd postgres -c "drop database if exists data_management_test"
psql $db_cmd postgres -c "create database data_management_test"
psql $db_cmd data_management_test -c "create extension postgis"

pg_dump -h pi -U djangotest -c --if-exists -O data_management | \
psql $db_cmd -d data_management_test
