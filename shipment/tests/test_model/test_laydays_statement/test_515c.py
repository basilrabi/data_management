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

pwd = dirname(abspath(__file__))
fdetails = join(pwd, 'detail', '515c.csv')


class  LayDaysStatement515CTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        setup_triggers()

    def setUp(self):
        vessel = Vessel(name='Gong Yin 1')
        vessel.save()
        shipment = Shipment(name='515-C', vessel=vessel)
        shipment.save()

    def test_laydays_computation_515c(self):
        shipment = Shipment.objects.get(name='515-C')
        statement = LayDaysStatement(
            shipment=shipment,
            arrival_pilot=pdt('2020-10-10 05:30:00+0800'),
            arrival_tmc=pdt('2020-10-10 12:18:00+0800'),
            nor_tender=pdt('2020-10-10 12:18:00+0800'),
            nor_accepted=pdt('2020-10-10 18:00:00+0800'),
            tonnage=51700,
            loading_terms=6000,
            demurrage_rate=15500,
            despatch_rate=7750,
            can_test=55
        )
        statement.save()
        self.assertEqual(
            statement.time_can_test(), timedelta(minutes=(2.5 * 55))
        )
        self.assertEqual(
            statement.time_limit(),
            timedelta(days=8, hours=17, minutes=5, seconds=30)
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
        statement = LayDaysStatement.objects.get(shipment__name='515-C')

        self.assertEqual(
            statement.completed_loading, pdt('2020-11-05 00:30:00+0800')
        )
        self.assertEqual(
            statement.commenced_laytime, pdt('2020-10-11 00:18:00+0800')
        )
        self.assertAlmostEqual(
            statement.laydaysdetailcomputed_set.all().last().time_remaining / one_day,
            -6.0149306,
            places=5
        )
        self.assertAlmostEqual(statement.demurrage, Decimal(93231.42), places=2)
        self.assertAlmostEqual(statement.despatch, Decimal(0), places=2)
        self.assertEqual(statement.clean(), None)
        approval = statement.approvedlaydaysstatement
        approval.approved = True
        approval.save()
        self.assertRaises(ValidationError, statement.clean)
