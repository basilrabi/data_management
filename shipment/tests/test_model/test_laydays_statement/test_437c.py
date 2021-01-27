import csv
from datetime import timedelta
from decimal import Decimal
from django.core.exceptions import ValidationError
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
fdetails = path.join(pwd, 'detail', '437c.csv')

class  LayDaysStatement437CTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        setup_triggers()

    def setUp(self):
        vessel = Vessel(name='Sheng Wang Hai')
        vessel.save()
        shipment = Shipment(name='437-C', vessel=vessel)
        shipment.save()

    def test_laydays_computation_437c(self):
        shipment = Shipment.objects.get(name='437-C')
        statement = LayDaysStatement(
            shipment=shipment,
            arrival_pilot=pdt('2019-08-28 15:30:00+0800'),
            arrival_tmc=pdt('2019-08-28 20:40:00+0800'),
            nor_tender=pdt('2019-08-28 20:40:00+0800'),
            nor_accepted=pdt('2019-08-30 21:30:00+0800'),
            tonnage=57200,
            loading_terms=6000,
            demurrage_rate=13000,
            despatch_rate=6500,
            can_test=24
        )
        statement.save()
        self.assertAlmostEqual(
            statement.time_can_test() / one_day, 0.04167, places=5
        )
        self.assertEqual(
            statement.time_limit(), timedelta(days=9, hours=13, minutes=48)
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
        statement = LayDaysStatement.objects.get(shipment__name='437-C')

        self.assertEqual(
            statement.completed_loading, pdt('2019-09-16 05:00:00+0800')
        )
        self.assertEqual(
            statement.commenced_laytime, pdt('2019-08-29 08:40:00+0800')
        )
        self.assertAlmostEqual(
            statement.laydaysdetailcomputed_set.all().last().time_remaining / one_day,
            -3.40069,
            places=5
        )
        self.assertAlmostEqual(statement.demurrage, Decimal(44209.03), places=2)
        self.assertAlmostEqual(statement.despatch, Decimal(0), places=2)
        self.assertEqual(statement.clean(), None)
        approval = statement.approvedlaydaysstatement
        approval.approved = True
        approval.save()
        self.assertRaises(ValidationError, statement.clean)
        shipment.refresh_from_db()
        self.assertAlmostEqual(shipment.demurrage, Decimal(44209.03))
        self.assertAlmostEqual(shipment.despatch, Decimal(0))
