import csv
from django.utils.dateparse import parse_datetime as pdt
from shipment.models.lct import Trip, TripDetail

with open('data/shipment_tripdetail.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # pylint: disable=E1101
        trip = Trip.objects.get(lct__name=row['trip_lct'],
                                interval_from=pdt(row['trip_interval_from']))
        detail = TripDetail(trip=trip,
                            interval_from=pdt(row['interval_from']),
                            interval_class=row['interval_class'],
                            remarks=row['remarks'])
        try:
            detail.clean()
            detail.save()
            print('TripDetail {} saved.'.format(detail.id))
        except:
            print('TripDetail {}:{} was not saved.'.format(
                detail.trip.lct.__str__(),
                str(detail.interval_from)
            ))
