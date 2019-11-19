import csv
from tzlocal import get_localzone
from shipment.models.lct import TripDetail

with open('data/shipment_tripdetail.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['trip_lct',
                     'trip_interval_from',
                     'interval_from',
                     'interval_class',
                     'remarks'])
    # pylint: disable=E1101
    for detail in TripDetail.objects.all().order_by('interval_from'):
        if detail.trip.tripdetail_set.all().count() > 1:
            writer.writerow([
                str(detail.trip.lct.name),
                str(detail.trip.interval_from.astimezone(get_localzone())),
                str(detail.interval_from.astimezone(get_localzone())),
                str(detail.interval_class),
                str(detail.remarks or '')
            ])
csvfile.close()
