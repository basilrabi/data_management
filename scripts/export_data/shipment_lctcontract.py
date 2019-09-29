import csv
from shipment.models.lct import LCTContract

with open('data/shipment_lctcontract.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['lct', 'start', 'end'])
    # pylint: disable=E1101
    for lct_contract in LCTContract.objects.all():
        writer.writerow([str(lct_contract.lct.name),
                         str(lct_contract.start),
                         str(lct_contract.end or '')])
csvfile.close()