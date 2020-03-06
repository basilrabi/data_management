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
            sys.exit(1)
        except Exception as e:
            print(f'Vessel {vessel.name} was not saved.')
            print(e)
            sys.exit(1)
        sys.stdout.flush()
        sys.stderr.flush()
