import csv
from shipment.models.dso import Shipment

with open('data/shipment_shipment.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['vessel',
                     'name',
                     'start_loading',
                     'end_loading',
                     'dump_truck_trips',
                     'tonnage'])
    # pylint: disable=E1101
    for shipment in Shipment.objects.all():
        writer.writerow([str(shipment.vessel.name),
                         str(shipment.name),
                         str(shipment.start_loading),
                         str(shipment.end_loading or ''),
                         str(shipment.dump_truck_trips),
                         str(shipment.tonnage)])
csvfile.close()