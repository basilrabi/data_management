# pylint: disable=import-error
# pylint: disable=no-member

from shipment.models.lct import Trip

print('Resaving all LCT trips...', flush=True)
trips = Trip.objects.all()
for trip in trips:
    print(f'Resaving {trip.lct.name}: {trip.interval_from}...', flush=True)
    trip.save()
print('Done.', flush=True)
