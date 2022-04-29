from csv import DictReader
from datetime import timedelta
from decimal import Decimal
from django.test import TestCase
from django.utils.dateparse import parse_datetime as pdt
from os.path import abspath, dirname, join

from custom.functions import setup_triggers
from custom.variables import one_day
from shipment.models.dso import (
    LayDaysDetail,
    LayDaysStatement,
    Shipment,
    Vessel
)

pwd = dirname(abspath(__file__))
fdetails = join(pwd, 'detail', '452c.csv')


class  LayDaysStatement452CTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        setup_triggers()

    def setUp(self):
        vessel = Vessel(name='Jia Yu Shan')
        vessel.save()
        shipment = Shipment(name='452-C', vessel=vessel)
        shipment.save()

    def test_laydays_computation_452c(self):
        shipment = Shipment.objects.get(name='452-C')
        statement = LayDaysStatement(
            shipment=shipment,
            arrival_pilot=pdt('2019-10-08 09:30:00+0800'),
            arrival_tmc=pdt('2019-10-08 17:48:00+0800'),
            nor_tender=pdt('2019-10-08 17:48:00+0800'),
            nor_accepted=pdt('2019-10-09 22:30:00+0800'),
            tonnage=56200,
            loading_terms=6000,
            demurrage_rate=19500,
            despatch_rate=9750,
            can_test=13
        )
        statement.save()
        self.assertAlmostEqual(
            statement.time_can_test() / one_day, 0.02257, places=5
        )
        self.assertEqual(
            statement.time_limit(),
            timedelta(days=9, hours=9, minutes=20, seconds=30)
        )

        with open(fdetails, newline='') as csvfile:
            reader = DictReader(
                csvfile,
                fieldnames=['rate', 'stamp', 'class', 'remarks']
            )
            for row in reader:
                LayDaysDetail(
                    laydays=statement,
                    laytime_rate=row['rate'],
                    interval_from=pdt(row['stamp']),
                    interval_class=row['class'],
                    remarks=row['remarks']
                ).save()

        statement._compute()
        statement = LayDaysStatement.objects.get(shipment__name='452-C')
        self.assertAlmostEqual(statement.demurrage,
                               Decimal(288457.81),
                               places=2)
