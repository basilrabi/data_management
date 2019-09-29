import csv
from django.utils.dateparse import parse_date as pd
from shipment.models.lct import LCT, LCTContract

with open('data/shipment_lctcontract.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # pylint: disable=E1101
        lct = LCT.objects.get(name=row['lct'])
        contract = LCTContract(
            lct=lct, start=pd(row['start']), end=pd(row['end'])
        )
        contract.save()
        print('Contract {} saved.'.format(contract.id))
