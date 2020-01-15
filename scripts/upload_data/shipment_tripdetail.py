import csv
import sys
from django.utils.dateparse import parse_datetime as pdt
from shipment.models.lct import Trip, TripDetail

# pylint: disable=no-member

with open('data/shipment_tripdetail.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['trip_lct',
                                                 'trip_interval_from',
                                                 'interval_from',
                                                 'interval_class',
                                                 'remarks'])
    for row in reader:
        trip = Trip.objects.get(lct__name=row['trip_lct'],
                                interval_from=pdt(row['trip_interval_from']))
        detail = TripDetail(trip=trip,
                            interval_from=pdt(row['interval_from']),
                            interval_class=row['interval_class'],
                            remarks=row['remarks'])
        try:
            detail.clean()
            detail.save(upload=True)
            print('TripDetail {} saved.'.format(detail.id))
        except KeyboardInterrupt:
            print('\nUploading interrupted.')
            break
        except:
            print('TripDetail {}:{} was not saved.'.format(
                detail.trip.lct.__str__(),
                str(detail.interval_from)
            ))
        sys.stdout.flush()
        sys.stderr.flush()

print('Resaving all LCT trips...')
for trip in Trip.objects.all():
    trip.save()
print('Done.')
