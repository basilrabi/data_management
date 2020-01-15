import csv
import sys
from shipment.models.lct import LCT

with open('data/shipment_lct.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['name', 'capacity'])
    for row in reader:
        # pylint: disable=E1101
        lct = LCT(name=row['name'], capacity=row['capacity'])
        try:
            lct.clean()
            lct.save()
            print('LCT {} saved.'.format(lct.id))
        except KeyboardInterrupt:
            print('\nUploading interrupted.')
            break
        except:
            print('LCT {} was not saved.'.format(lct.name))
        sys.stdout.flush()
        sys.stderr.flush()
