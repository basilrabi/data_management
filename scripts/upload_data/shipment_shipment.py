import csv
from django.utils.dateparse import parse_datetime as pdt
from shipment.models.dso import Shipment, Vessel

with open('data/shipment_shipment.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # pylint: disable=E1101
        vessel = Vessel.objects.get(name=row['vessel'])
        shipment = Shipment(name=row['name'],
                            start_loading=pdt(row['start_loading']),
                            end_loading=pdt(row['end_loading']),
                            dump_truck_trips=row['dump_truck_trips'],
                            tonnage=row['tonnage'],
                            vessel=vessel)
        shipment.save()
        print('Shipment {} saved.'.format(shipment.id))
