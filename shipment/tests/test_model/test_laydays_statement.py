from datetime import timedelta
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.dateparse import parse_datetime as pdt

from custom.variables import day_time
from shipment.models.dso import (LayDaysDetail,
                                 LayDaysStatement,
                                 Shipment,
                                 Vessel)

class  LayDaysStatementTest(TestCase):

    def setUp(self):
        vessel = Vessel(name='Chang Shun II')
        vessel.save()
        shipment = Shipment(
            name='431-C', vessel=vessel,
            start_loading=pdt('2019-08-17 00:00:00+0800'),
            end_loading=pdt('2019-08-19 00:00:00+0800')
        )
        shipment.save()

    def test_arrival_at_tmc_should_be_later_than_arrival_at_surigao(self):
        shipment = Shipment.objects.all().first() # pylint: disable=E1101
        statement = LayDaysStatement(
            shipment=shipment,
            arrival_pilot=pdt('2019-08-16 12:00:00+0800'),
            arrival_tmc=pdt('2019-08-16 00:00:00+0800')
        )
        self.assertRaises(ValidationError, statement.clean)
        statement = LayDaysStatement(
            shipment=shipment,
            arrival_pilot=pdt('2019-08-16 00:00:00+0800'),
            arrival_tmc=pdt('2019-08-16 12:00:00+0800')
        )
        self.assertEqual(statement.clean(), None)

    def test_nor_tender_should_be_later_than_acceptance(self):
        shipment = Shipment.objects.all().first() # pylint: disable=E1101
        statement = LayDaysStatement(
            shipment=shipment,
            nor_tender=pdt('2019-08-16 12:00:00+0800'),
            nor_accepted=pdt('2019-08-16 00:00:00+0800')
        )
        self.assertRaises(ValidationError, statement.clean)
        statement = LayDaysStatement(
            shipment=shipment,
            nor_tender=pdt('2019-08-16 00:00:00+0800'),
            nor_accepted=pdt('2019-08-16 12:00:00+0800')
        )
        self.assertEqual(statement.clean(), None)

    def test_nor_tender_not_earlier_than_arrival_at_tmc(self):
        shipment = Shipment.objects.all().first() # pylint: disable=E1101
        statement = LayDaysStatement(
            shipment=shipment,
            arrival_tmc=pdt('2019-08-16 12:00:00+0800'),
            nor_tender=pdt('2019-08-16 00:00:00+0800')
        )
        self.assertRaises(ValidationError, statement.clean)
        statement = LayDaysStatement(
            shipment=shipment,
            arrival_tmc=pdt('2019-08-16 00:00:00+0800'),
            nor_tender=pdt('2019-08-16 00:00:00+0800')
        )
        self.assertEqual(statement.clean(), None)

    def test_laydays_computation_431c(self):
        # pylint: disable=E1101
        shipment = Shipment.objects.all().first()
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
        self.assertAlmostEqual(statement.time_can_test(), 0.03819, places=5)
        self.assertAlmostEqual(
            statement.time_limit(),
            timedelta(days=9, hours=5, minutes=19) / day_time,
            places=5
        )

        detail = LayDaysDetail(
            laydays=statement, loading_rate=100,
            interval_from=pdt('2019-08-12 02:50:00+0800'),
            interval_class='loading',
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, loading_rate=100,
            interval_from=pdt('2019-08-12 08:20:00+0800'),
            interval_class='waiting_for_cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, loading_rate=0,
            interval_from=pdt('2019-08-12 15:05:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, loading_rate=100,
            interval_from=pdt('2019-08-12 17:35:00+0800'),
            interval_class='waiting_for_cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, loading_rate=100,
            interval_from=pdt('2019-08-12 19:10:00+0800'),
            interval_class='loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, loading_rate=0,
            interval_from=pdt('2019-08-12 19:55:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, loading_rate=100,
            interval_from=pdt('2019-08-12 21:00:00+0800'),
            interval_class='loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, loading_rate=100,
            interval_from=pdt('2019-08-12 23:45:00+0800'),
            interval_class='waiting_for_cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, loading_rate=100,
            interval_from=pdt('2019-08-13 13:50:00+0800'),
            interval_class='loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, loading_rate=100,
            interval_from=pdt('2019-08-13 18:20:00+0800'),
            interval_class='waiting_for_cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, loading_rate=0,
            interval_from=pdt('2019-08-13 22:30:00+0800'),
            interval_class='swell'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, loading_rate=100,
            interval_from=pdt('2019-08-14 01:30:00+0800'),
            interval_class='loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, loading_rate=100,
            interval_from=pdt('2019-08-14 09:40:00+0800'),
            interval_class='waiting_for_cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, loading_rate=100,
            interval_from=pdt('2019-08-14 12:50:00+0800'),
            interval_class='loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, loading_rate=100,
            interval_from=pdt('2019-08-16 18:55:00+0800'),
            interval_class='waiting_for_cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, loading_rate=100,
            interval_from=pdt('2019-08-16 21:40:00+0800'),
            interval_class='loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, loading_rate=100,
            interval_from=pdt('2019-08-17 02:00:00+0800'),
            interval_class='waiting_for_cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, loading_rate=100,
            interval_from=pdt('2019-08-17 05:50:00+0800'),
            interval_class='loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, loading_rate=100,
            interval_from=pdt('2019-08-17 21:40:00+0800'),
            interval_class='waiting_for_cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, loading_rate=100,
            interval_from=pdt('2019-08-18 03:10:00+0800'),
            interval_class='loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, loading_rate=100,
            interval_from=pdt('2019-08-18 15:00:00+0800'),
            interval_class='end'
        )
        detail.save()
        statement.save()
        statement = LayDaysStatement.objects.all().first()
        self.assertAlmostEqual(
            statement.laytime_difference(), Decimal(2.98889), places=5
        )
        self.assertAlmostEqual(statement.demurrage, Decimal(0), places=2)
        self.assertAlmostEqual(statement.despatch, Decimal(16438.90), places=2)
