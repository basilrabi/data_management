from datetime import timedelta
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.dateparse import parse_datetime as pdt

from custom.variables import one_day
from shipment.models.dso import (LayDaysDetail,
                                 LayDaysStatement,
                                 Shipment,
                                 Vessel)

# pylint: disable=no-member

class  LayDaysStatement476CTest(TestCase):

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
        self.assertAlmostEqual(
            statement.time_limit(), timedelta(days=9, hours=4, minutes=27)
        )

        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-06-24 00:30:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-06-24 04:35:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-06-24 15:00:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-06-24 22:10:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-06-25 00:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-06-25 04:00:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-06-25 13:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-06-25 15:30:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-06-25 16:05:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-06-25 16:40:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-06-26 08:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-06-26 12:50:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-06-26 23:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-06-27 09:00:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-06-27 20:20:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-06-27 20:30:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-06-28 04:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-06-28 19:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-06-28 20:20:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-06-28 22:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-06-29 08:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-06-29 22:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-06-30 08:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-01 04:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-01 07:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-01 15:15:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-01 17:20:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-01 22:50:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-02 08:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-02 10:35:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-02 17:35:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-02 22:40:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-03 00:40:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-03 04:45:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-03 08:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-03 12:55:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-03 15:50:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-03 20:30:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-04 01:35:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-04 08:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-04 13:40:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-04 15:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-04 18:35:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-05 03:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-05 04:20:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-05 05:30:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-05 11:00:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-06 05:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-06 07:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-06 13:35:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-06 20:30:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-07 04:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-07 06:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-07 09:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-07 10:30:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-07 12:30:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-07 15:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-07 19:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-08 01:25:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-08 04:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-08 09:30:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-08 10:30:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-08 16:05:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-08 21:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-09 00:30:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-09 06:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-09 20:15:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-10 01:30:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-10 16:55:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-10 18:30:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2020-07-10 23:30:00+0800'),
            interval_class='end'
        )
        detail.save()

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
