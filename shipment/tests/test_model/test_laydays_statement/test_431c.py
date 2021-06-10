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
fdetails = join(pwd, 'detail', '431c.csv')


class  LayDaysStatement431CTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        setup_triggers()

    def setUp(self):
        vessel = Vessel(name='Chang Shun II')
        vessel.save()
        shipment = Shipment(
            name='431-C',
            vessel=vessel,
            demurrage=0,
            despatch=Decimal(16438.89)
        )
        shipment.save()

    def test_laydays_computation_431c(self):
        shipment = Shipment.objects.get(name='431-C')
        statement = LayDaysStatement(
            shipment=shipment,
            arrival_pilot=pdt('2019-08-11 12:30:00+0800'),
            arrival_tmc=pdt('2019-08-11 17:00:00+0800'),
            nor_tender=pdt('2019-08-11 17:00:00+0800'),
            nor_accepted=pdt('2019-08-11 19:45:00+0800'),
            tonnage=55100,
            loading_terms=6000,
            demurrage_rate=11000,
            despatch_rate=5500,
            can_test=22
        )
        statement.save()
        self.assertAlmostEqual(
            statement.time_can_test() / one_day, 0.03819, places=5
        )
        self.assertEqual(
            statement.time_limit(), timedelta(days=9, hours=5, minutes=19)
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
        statement = LayDaysStatement.objects.get(shipment__name='431-C')

        self.assertEqual(
            statement.completed_loading, pdt('2019-08-18 15:00:00+0800')
        )
        self.assertEqual(
            statement.commenced_laytime, pdt('2019-08-12 02:50:00+0800')
        )
        self.assertAlmostEqual(
            statement.laydaysdetailcomputed_set.all().last().time_remaining / one_day,
            2.98889,
            places=5
        )
        self.assertAlmostEqual(statement.demurrage, Decimal(0), places=2)
        self.assertAlmostEqual(statement.despatch, Decimal(16438.89), places=2)
        self.assertEqual(statement.clean(), None)
        approval = statement.approvedlaydaysstatement
        approval.approved = True
        approval.save()
        self.assertRaises(ValidationError, statement.clean)
        shipment.refresh_from_db()
        shipment.demurrage = Decimal(0)
        self.assertEqual(shipment.clean(), None)
        shipment.despatch = Decimal(0)
        self.assertRaises(ValidationError, shipment.clean)
