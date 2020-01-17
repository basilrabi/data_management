import csv
import sys
from shipment.models.lct import LCT
# pylint: disable=no-member
with open('data/shipment_lct.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['name', 'capacity'])
    for row in reader:
        lct = LCT(name=row['name'], capacity=row['capacity'])
        try:
            lct.clean()
            lct.save()
            print(f'LCT {lct.id} saved.')
        except KeyboardInterrupt:
            print('\nUploading interrupted.')
            break
        except:
            print(f'LCT {lct.name} was not saved.')
        sys.stdout.flush()
        sys.stderr.flush()
