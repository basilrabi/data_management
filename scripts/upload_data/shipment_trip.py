import csv
import sys
from shipment.models.dso import Vessel
from shipment.models.lct import LCT, Trip
# pylint: disable=no-member
with open('data/shipment_trip.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['lct',
                                                 'vessel',
                                                 'status',
                                                 'dump_truck_trips',
                                                 'vessel_grab',
                                                 'interval_from'])
    for row in reader:
        lct = LCT.objects.get(name=row['lct'])
        vessel = Vessel.objects.get(name=row['vessel'])
        if row['interval_from'] != '':
            trip = Trip(lct=lct,
                        vessel=vessel,
                        status=row['status'],
                        dump_truck_trips=int(row['dump_truck_trips']),
                        vessel_grab=int(row['vessel_grab']),
                        interval_from=row['interval_from'])
        else:
            trip = Trip(lct=lct,
                        vessel=vessel,
                        status=row['status'],
                        dump_truck_trips=int(row['dump_truck_trips']),
                        vessel_grab=int(row['vessel_grab']))
        try:
            trip.clean()
            trip.save()
            print(f'Trip {trip.id} saved.')
        except KeyboardInterrupt:
            print('\nUploading interrupted.')
            sys.exit(1)
        except Exception as e:
            print(f'Trip {trip.lct.__str__()}-{trip.vessel.__str__()} was not saved.')
            print(e)
            sys.exit(1)
        sys.stdout.flush()
        sys.stderr.flush()
