import csv
from shipment.models.dso import Vessel

with open('data/shipment_vessel.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # pylint: disable=E1101
        vessel = Vessel(name=row['name'])
        vessel.save()
        print('Vessel {} saved.'.format(vessel.id))