import csv
from shipment.models.dso import Vessel
from shipment.models.lct import LCT, Trip

with open('data/shipment_trip.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # pylint: disable=E1101
        lct = LCT.objects.get(id=row['lct_id'])
        vessel = Vessel.objects.get(id=row['vessel_id'])
        trip = Trip(lct=lct,
                    vessel=vessel,
                    status=row['status'],
                    dump_truck_trips=row['dump_truck_trips'],
                    vessel_grab=row['vessel_grab'])
        trip.save()
        print('Trip {} saved.'.format(trip.id))
