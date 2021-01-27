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
fdetails = path.join(pwd, 'detail', '522c.csv')

class  LayDaysStatement522CTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        setup_triggers()

    def setUp(self):
        vessel = Vessel(name='Jin Ping')
        vessel.save()
        shipment = Shipment(name='522-C', vessel=vessel)
        shipment.save()

    def test_laydays_computation_522c(self):
        shipment = Shipment.objects.get(name='522-C')
        statement = LayDaysStatement(
            shipment=shipment,
            arrival_pilot=pdt('2020-11-05 06:00:00+0800'),
            arrival_tmc=pdt('2020-11-05 12:36:00+0800'),
            nor_tender=pdt('2020-11-05 12:36:00+0800'),
            nor_accepted=pdt('2020-11-05 17:00:00+0800'),
            tonnage=40160,
            loading_terms=10,
            demurrage_rate=13000,
            despatch_rate=6500,
            can_test=0,
            laytime_terms='CQD'
        )
        statement.save()
        self.assertAlmostEqual(statement.time_can_test() / one_day, 0, places=5)
        self.assertEqual(statement.time_limit(), timedelta(days=10))

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
        statement = LayDaysStatement.objects.get(shipment__name='522-C')

        self.assertEqual(
            statement.completed_loading, pdt('2020-11-25 01:00:00+0800')
        )
        self.assertEqual(
            statement.commenced_laytime, pdt('2020-11-06 00:36:00+0800')
        )
        self.assertAlmostEqual(
            statement.laydaysdetailcomputed_set.all().last().time_remaining / one_day,
            -9.01667,
            places=5
        )
        self.assertAlmostEqual(statement.demurrage, Decimal(117216.67), places=2)
        self.assertAlmostEqual(statement.despatch, Decimal(0), places=2)
        self.assertEqual(statement.clean(), None)
        approval = statement.approvedlaydaysstatement
        approval.approved = True
        approval.save()
        self.assertRaises(ValidationError, statement.clean)
