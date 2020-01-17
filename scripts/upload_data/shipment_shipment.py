import csv
import sys
from django.utils.dateparse import parse_datetime as pdt
from shipment.models.dso import Shipment, Vessel
# pylint: disable=no-member
with open('data/shipment_shipment.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['vessel',
                                                 'name',
                                                 'start_loading',
                                                 'end_loading',
                                                 'dump_truck_trips',
                                                 'tonnage'])
    for row in reader:
        vessel = Vessel.objects.get(name=row['vessel'])
        shipment = Shipment(name=row['name'],
                            start_loading=pdt(row['start_loading']),
                            end_loading=pdt(row['end_loading']),
                            dump_truck_trips=row['dump_truck_trips'],
                            tonnage=row['tonnage'],
                            vessel=vessel)
        try:
            shipment.clean()
            shipment.save()
            print(f'Shipment {shipment.id} saved.')
        except KeyboardInterrupt:
            print('\nUploading interrupted.')
            break
        except:
            print(f'Shipment {shipment.name} was not saved.')
        sys.stdout.flush()
        sys.stderr.flush()
