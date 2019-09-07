#!/usr/bin/bash

./manage.py shell < scripts/upload_data/shipment_lct.py
./manage.py shell < scripts/upload_data/shipment_lctcontract.py
./manage.py shell < scripts/upload_data/shipment_vessel.py
./manage.py shell < scripts/upload_data/shipment_shipment.py
./manage.py shell < scripts/upload_data/shipment_trip.py
./manage.py shell < scripts/upload_data/shipment_tripdetail.py
