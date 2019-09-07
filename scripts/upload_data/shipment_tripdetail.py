import csv
from django.utils.dateparse import parse_datetime as pdt
from shipment.models.lct import Trip, TripDetail

with open('data/shipment_tripdetail.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # pylint: disable=E1101
        trip = Trip.objects.get(id=row['trip_id'])
        detail = TripDetail(trip=trip,
                            interval_from=pdt(row['interval_from']),
                            interval_class=row['interval_class'],
                            remarks=row['remarks'])
        detail.save()
        print('TripDetial {} saved.'.format(detail.id))
