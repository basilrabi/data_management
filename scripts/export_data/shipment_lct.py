import csv
from shipment.models.lct import LCT

with open('data/shipment_lct.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['name', 'capacity'])
    # pylint: disable=E1101
    for lct in LCT.objects.all():
        writer.writerow([str(lct.name), str(lct.capacity)])
csvfile.close()