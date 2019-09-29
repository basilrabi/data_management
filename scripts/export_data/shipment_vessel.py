import csv
from shipment.models.dso import Vessel

with open('data/shipment_vessel.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['name'])
    # pylint: disable=E1101
    for vessel in Vessel.objects.all():
        writer.writerow([str(vessel.name)])
csvfile.close()