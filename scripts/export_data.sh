#!/usr/bin/bash

rm data -rf
mkdir data

db_cmd='-h tmc -U data_management data_management'

psql $db_cmd -c "\copy shipment_lct to 'data/shipment_lct.csv' csv header"
psql $db_cmd -c "\copy shipment_lctcontract to 'data/shipment_lctcontract.csv' csv header"
psql $db_cmd -c "\copy shipment_shipment to 'data/shipment_shipment.csv' csv header"
psql $db_cmd -c "\copy shipment_trip to 'data/shipment_trip.csv' csv header"
psql $db_cmd -c "\copy shipment_tripdetail to 'data/shipment_tripdetail.csv' csv header"
psql $db_cmd -c "\copy shipment_vessel to 'data/shipment_vessel.csv' csv header"
