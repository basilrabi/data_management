# pylint: disable=import-error
# pylint: disable=no-member

import csv
import sys
from django.utils.dateparse import parse_datetime as pdt
from shipment.models.dso import Shipment, Vessel

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
                            dump_truck_trips=row['dump_truck_trips'],
                            vessel=vessel)
        try:
            shipment.clean()
            shipment.save()
            print(f'Shipment {shipment.id} saved.')
        except KeyboardInterrupt:
            print('\nUploading interrupted.')
            sys.exit(1)
        except Exception as e:
            print(f'Shipment {shipment.name} was not saved.')
            print(e)
            sys.exit(1)
        sys.stdout.flush()
        sys.stderr.flush()
