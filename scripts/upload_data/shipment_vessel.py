import csv
import sys
from shipment.models.dso import Vessel
# pylint: disable=no-member
with open('data/shipment_vessel.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['name'])
    for row in reader:
        vessel = Vessel(name=row['name'])
        try:
            vessel.clean()
            vessel.save()
            print(f'Vessel {vessel.id} saved.')
        except KeyboardInterrupt:
            print('\nUploading interrupted.')
            break
        except:
            print(f'Vessel {vessel.name} was not saved.')
        sys.stdout.flush()
        sys.stderr.flush()
