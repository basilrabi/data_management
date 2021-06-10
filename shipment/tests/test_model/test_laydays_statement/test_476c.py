from csv import DictReader
from datetime import timedelta
from decimal import Decimal
from django.core.exceptions import ValidationError
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

# pylint: disable=no-member

pwd = dirname(abspath(__file__))
fdetails = join(pwd, 'detail', '476c.csv')


class  LayDaysStatement476CTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        setup_triggers()

    def setUp(self):
        vessel = Vessel(name='Jin Yue')
        vessel.save()
        shipment = Shipment(name='476-C', vessel=vessel)
        shipment.save()

    def test_laydays_computation_476c(self):
        shipment = Shipment.objects.get(name='476-C')
        statement = LayDaysStatement(
            shipment=shipment,
            arrival_pilot=pdt('2020-06-23 06:00:00+0800'),
            arrival_tmc=pdt('2020-06-23 12:30:00+0800'),
            nor_tender=pdt('2020-06-23 12:30:00+0800'),
            nor_accepted=pdt('2020-06-23 15:00:00+0800'),
            tonnage=54800,
            loading_terms=6000,
            demurrage_rate=10500,
            despatch_rate=5250,
            can_test=30
        )
        statement.save()
        self.assertAlmostEqual(
            statement.time_can_test() / one_day, 0.05208, places=5
        )
        self.assertEqual(
            statement.time_limit(), timedelta(days=9, hours=4, minutes=27)
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
        statement = LayDaysStatement.objects.get(shipment__name='476-C')

        self.assertEqual(
            statement.completed_loading, pdt('2020-07-10 23:30:00+0800')
        )
        self.assertEqual(
            statement.commenced_laytime, pdt('2020-06-24 00:30:00+0800')
        )
        self.assertAlmostEqual(
            statement.laydaysdetailcomputed_set.all().last().time_remaining / one_day,
            -2.79375,
            places=5
        )
        self.assertAlmostEqual(statement.demurrage, Decimal(29334.38), places=2)
        self.assertAlmostEqual(statement.despatch, Decimal(0), places=2)
        self.assertEqual(statement.clean(), None)
        approval = statement.approvedlaydaysstatement
        approval.approved = True
        approval.save()
        self.assertRaises(ValidationError, statement.clean)
