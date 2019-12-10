import csv
from shipment.models.dso import Vessel
from shipment.models.lct import LCT, Trip

with open('data/shipment_trip.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['lct',
                                                 'vessel',
                                                 'status',
                                                 'dump_truck_trips',
                                                 'vessel_grab',
                                                 'interval_from',
                                                 'interval_to'])
    for row in reader:
        # pylint: disable=E1101
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
            print('Trip {} saved.'.format(trip.id))
        except KeyboardInterrupt:
            print('\nUploading interrupted.')
            break
        except:
            print('Trip {}-{} was not saved.'.format(
                trip.lct.__str__(), trip.vessel.__str__()
            ))
