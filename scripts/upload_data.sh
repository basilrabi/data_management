#!/usr/bin/bash

set -a
. data_management/local.py
set +a

ogr2ogr -update -append \
    -f PostgreSQL "PG:host=$db_host port=$db_port user=$db_user dbname=$db_name password=$db_password" \
    -fieldmap 0,1 \
    -nln location_mineblock data/location_mineblock.gpkg

./manage.py shell < scripts/upload_data/shipment_lct.py && \
echo "Uploading shipment.LCT success." && \
./manage.py shell < scripts/upload_data/shipment_lctcontract.py && \
echo "Uploading shipment.LCTContract success." && \
./manage.py shell < scripts/upload_data/shipment_vessel.py && \
echo "Uploading shipment.Vessel success." && \
./manage.py shell < scripts/upload_data/shipment_shipment.py && \
echo "Uploading shipment.Shipment success." && \
./manage.py shell < scripts/upload_data/shipment_laydaysstatement.py && \
echo "Uploading shipment.LayDaysStatement success." && \
./manage.py shell < scripts/upload_data/shipment_laydaysdetail.py && \
echo "Uploading shipment.LayDaysDetail success." && \
./manage.py shell < scripts/upload_data/shipment_trip.py && \
echo "Uploading shipment.Trip success." && \
./manage.py shell < scripts/upload_data/shipment_tripdetail.py && \
echo "Uploading shipment.TripDetail success."
