import csv
from shipment.models.lct import LCT

with open('data/shipment_lct.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # pylint: disable=E1101
        lct = LCT(name=row['name'], capacity=row['capacity'])
        lct.save()
        print('LCT {} saved.'.format(lct.id))
