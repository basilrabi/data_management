import csv
import sys
from django.utils.dateparse import parse_date as pd, parse_datetime as pdt
from shipment.models.dso import LayDaysStatement, Shipment

with open('data/shipment_laydaysstatement.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['shipment',
                                                 'vessel_voyage',
                                                 'arrival_pilot',
                                                 'arrival_tmc',
                                                 'nor_tender',
                                                 'nor_accepted',
                                                 'cargo_description',
                                                 'tonnage',
                                                 'loading_terms',
                                                 'demurrage_rate',
                                                 'despatch_rate',
                                                 'can_test',
                                                 'pre_loading_can_test',
                                                 'report_date',
                                                 'revised'])
    for row in reader:
        # pylint: disable=E1101
        shipment = Shipment.objects.get(name=row['shipment'])
        statement = LayDaysStatement(
            shipment=shipment,
            vessel_voyage=int(row['vessel_voyage']),
            arrival_pilot=pdt(row['arrival_pilot']),
            arrival_tmc=pdt(row['arrival_tmc']),
            nor_tender=pdt(row['nor_tender']),
            nor_accepted=pdt(row['nor_accepted']),
            cargo_description=row['cargo_description'],
            tonnage=int(row['tonnage'] or 0),
            loading_terms=int(row['loading_terms']),
            demurrage_rate=int(row['demurrage_rate']),
            despatch_rate=int(row['despatch_rate']),
            can_test=int(row['can_test']),
            pre_loading_can_test=row['pre_loading_can_test'],
            report_date=pd(row['report_date']),
            revised=row['revised']
        )
        try:
            statement.clean()
            statement.save()
            print(f'Lay Days Statement {statement.shipment.__str__()} saved.')
        except KeyboardInterrupt:
            print('\nUploading interrupted.')
            break
        except:
            print('Lay Days Statement of shipment ' + \
                f'{statement.shipment.__str__()} was not saved.')
        sys.stdout.flush()
        sys.stderr.flush()
