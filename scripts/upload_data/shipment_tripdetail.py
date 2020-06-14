# pylint: disable=import-error
# pylint: disable=no-member

import csv
import sys
from shipment.models.lct import Trip

print('Resaving all LCT trips...', flush=True)
trips = Trip.objects.all()
for trip in trips:
    print(f'Resaving {trip.lct.name}: {trip.interval_from}...')
    sys.stdout.flush()
    sys.stderr.flush()
    trip.save()
print('Done.')
