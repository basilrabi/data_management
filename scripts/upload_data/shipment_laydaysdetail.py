import csv
from django.utils.dateparse import parse_datetime as pdt
from shipment.models.dso import LayDaysDetail, LayDaysStatement

# pylint: disable=no-member

with open('data/shipment_laydaysdetail.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['shipment',
                                                 'interval_from',
                                                 'loading_rate',
                                                 'interval_class',
                                                 'remarks',
                                                 'can_test'])
    for row in reader:
        statement = LayDaysStatement.objects \
            .get(shipment__name=row['shipment'])
        detail = LayDaysDetail(laydays=statement,
                               interval_from=pdt(row['interval_from']),
                               loading_rate=int(row['loading_rate']),
                               interval_class=row['interval_class'],
                               remarks=row['remarks'],
                               can_test=row['can_test'])
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

for statement in LayDaysStatement.objects.all():
    try:
        statement._compute()
        print(f'Statement for {statement.__str__()} done.')
    except KeyboardInterrupt:
        print('\nComputing statement interrupted.')
        break
