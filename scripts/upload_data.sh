#!/usr/bin/bash

./manage.py shell < scripts/upload_data/shipment_lct.py && \
echo "Uploading shipment.LCT success." && \
./manage.py shell < scripts/upload_data/shipment_lctcontract.py && \
echo "Uploading shipment.LCTContract success." && \
./manage.py shell < scripts/upload_data/shipment_vessel.py && \
echo "Uploading shipment.Vessel success." && \
./manage.py shell < scripts/upload_data/shipment_shipment.py && \
echo "Uploading shipment.Shipment success." && \
./manage.py shell < scripts/upload_data/shipment_trip.py && \
echo "Uploading shipment.Trip success." && \
./manage.py shell < scripts/upload_data/shipment_tripdetail.py && \
echo "Uploading shipment.TripDetail success."
