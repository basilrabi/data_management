import csv
from datetime import timedelta
from decimal import Decimal
from django.test import TestCase
from django.utils.dateparse import parse_datetime as pdt
from os import path

from custom.functions import setup_triggers
from custom.variables import one_day
from shipment.models.dso import (LayDaysDetail,
                                 LayDaysStatement,
                                 Shipment,
                                 Vessel)

# pylint: disable=no-member

pwd = path.dirname(path.abspath(__file__))
fdetails = path.join(pwd, 'detail', '453c.csv')

class  LayDaysStatement453CTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        setup_triggers()

    def setUp(self):
        vessel = Vessel(name='Sheng Heng Hai')
        vessel.save()
        shipment = Shipment(name='453-C', vessel=vessel)
        shipment.save()

    def test_laydays_computation_453c(self):
        shipment = Shipment.objects.get(name='453-C')
        statement = LayDaysStatement(
            shipment=shipment,
            arrival_pilot=pdt('2019-10-11 06:42:00+0800'),
            arrival_tmc=pdt('2019-10-11 11:55:00+0800'),
            nor_tender=pdt('2019-10-11 11:55:00+0800'),
            nor_accepted=pdt('2019-10-14 21:00:00+0800'),
            tonnage=55100,
            loading_terms=6000,
            demurrage_rate=20500,
            despatch_rate=10250,
            can_test=9,
            can_test_factor=1
        )
        statement.save()
        self.assertAlmostEqual(
            statement.time_can_test() / one_day, 0.03125, places=5
        )
        self.assertEqual(
            statement.time_limit(), timedelta(days=9, hours=5, minutes=9)
        )

        with open(fdetails, newline='') as csvfile:
            reader = csv.DictReader(
                csvfile,
                fieldnames=['rate', 'stamp', 'class']
            )
            for row in reader:
                LayDaysDetail(
                    laydays=statement,
                    laytime_rate=row['rate'],
                    interval_from=pdt(row['stamp']),
                    interval_class=row['class']
                ).save()

        statement._compute()
        statement = LayDaysStatement.objects.get(shipment__name='453-C')
        self.assertAlmostEqual(statement.demurrage,
                               Decimal(288423.61),
                               places=2)
