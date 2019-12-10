import csv

from django.utils.dateparse import parse_datetime as pdt

from shipment.models.dso import LayDaysDetail, LayDaysStatement

with open('data/shipment_laydaysdetail.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['shipment',
                                                 'interval_from',
                                                 'loading_rate',
                                                 'interval_class',
                                                 'remarks',
                                                 'pause_override'])
    for row in reader:
        # pylint: disable=E1101
        statement = LayDaysStatement.objects \
            .get(shipment__name=row['shipment'])
        detail = LayDaysDetail(laydays=statement,
                               interval_from=pdt(row['interval_from']),
                               loading_rate=int(row['loading_rate']),
                               interval_class=row['interval_class'],
                               remarks=row['remarks'],
                               pause_override=row['pause_override'])
        try:
            detail.clean()
            detail.save()
            print(f'LayDaysDetail {detail.id} saved.')
        except KeyboardInterrupt:
            print('\nUploading interrupted.')
            break
        except:
            print('LayDaysDetail {}:{} was not saved.'.format(
                detail.laydays.shipment.__str__(),
                str(detail.interval_from)
            ))
