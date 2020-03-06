import csv
import sys
from django.utils.dateparse import parse_date as pd
from shipment.models.lct import LCT, LCTContract
# pylint: disable=no-member
with open('data/shipment_lctcontract.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['lct', 'start', 'end'])
    for row in reader:
        lct = LCT.objects.get(name=row['lct'])
        contract = LCTContract(
            lct=lct, start=pd(row['start']), end=pd(row['end'])
        )
        try:
            contract.clean()
            contract.save()
            print(f'Contract {contract.id} saved.')
        except KeyboardInterrupt:
            print('\nUploading interrupted.')
            sys.exit(1)
        except Exception as e:
            print(f'Contract {contract.lct.__str__()}:{str(contract.start)} was not saved.')
            print(e)
            sys.exit(1)
        sys.stdout.flush()
        sys.stderr.flush()
