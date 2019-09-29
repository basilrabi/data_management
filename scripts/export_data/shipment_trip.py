import csv
from shipment.models.lct import Trip

with open('data/shipment_trip.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['lct',
                     'vessel',
                     'status',
                     'dump_truck_trips',
                     'vessel_grab',
                     'interval_from',
                     'interval_to',
                     'valid'])
    # pylint: disable=E1101
    for trip in Trip.objects.all():
        vessel = ''
        if trip.vessel:
            vessel = trip.vessel.name
        writer.writerow([str(trip.lct.name),
                         str(vessel),
                         str(trip.status),
                         str(trip.dump_truck_trips),
                         str(trip.vessel_grab),
                         str(trip.interval_from or ''),
                         str(trip.interval_to or ''),
                         str(trip.valid)])
csvfile.close()