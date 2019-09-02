#!/usr/bin/bash

db_cmd='psql -h localhost -U djangotest postgres -c'

$db_cmd "drop database if exists data_management_test"
$db_cmd "create database data_management_test"
