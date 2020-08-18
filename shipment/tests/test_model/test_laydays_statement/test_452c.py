from datetime import timedelta
from decimal import Decimal
from django.test import TestCase
from django.utils.dateparse import parse_datetime as pdt

from custom.functions import setup_triggers
from custom.variables import one_day
from shipment.models.dso import (LayDaysDetail,
                                 LayDaysStatement,
                                 Shipment,
                                 Vessel)

# pylint: disable=no-member

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
        self.assertAlmostEqual(
            statement.time_limit() / one_day,
            timedelta(days=9, hours=9, minutes=20, seconds=30) / one_day,
            places=5
        )

        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-09 05:48:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-10 23:50:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-11 13:30:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-11 19:30:00+0800'),
            interval_class='heavy swell'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-10-11 23:15:00+0800'),
            interval_class='waiting for cargo due to rejection'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-12 00:00:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-12 17:20:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=75,
            interval_from=pdt('2019-10-13 01:30:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-13 08:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-13 10:40:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=50,
            interval_from=pdt('2019-10-14 04:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-14 06:00:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-14 06:40:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=25,
            interval_from=pdt('2019-10-14 07:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-14 09:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-14 18:05:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-10-14 20:30:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-15 12:40:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-10-15 18:20:00+0800'),
            interval_class='waiting for cargo due to rejection'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-10-15 19:10:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-15 21:30:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-10-16 02:20:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-16 08:00:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-10-16 11:30:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-16 13:15:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-16 14:20:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-16 18:00:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-10-16 21:30:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-17 10:00:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-10-17 15:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-18 08:05:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-10-18 16:25:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-18 20:20:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-19 09:30:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-19 11:55:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-19 16:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-10-19 16:30:00+0800'),
            interval_class='heavy swell'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-19 18:40:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-19 21:15:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-20 00:20:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-20 03:10:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-10-20 21:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-20 22:00:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-10-20 22:30:00+0800'),
            interval_class='waiting for cargo due to rejection'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-21 00:00:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-21 03:35:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-21 23:04:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-22 02:10:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-22 03:40:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-22 04:40:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-22 11:40:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-22 17:55:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-23 00:05:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-23 01:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-23 03:10:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-23 14:30:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-23 18:35:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-23 20:50:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-24 04:00:00+0800'),
            interval_class='heavy swell'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-24 07:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-10-24 08:00:00+0800'),
            interval_class='sun drying'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-24 09:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-10-24 11:10:00+0800'),
            interval_class='sun drying'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-24 13:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-10-24 14:10:00+0800'),
            interval_class='sun drying'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-24 16:30:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-24 22:35:00+0800'),
            interval_class='heavy swell'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-25 00:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-25 07:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-25 14:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-25 15:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-25 15:30:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-26 00:00:00+0800'),
            interval_class='rain and heavy swell'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-27 00:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-28 03:00:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-28 13:30:00+0800'),
            interval_class='rain and heavy swell'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-28 18:00:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-28 21:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-29 07:00:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-29 21:40:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-30 02:15:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-30 04:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-31 15:40:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-01 03:10:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-01 10:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-01 12:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-01 19:40:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-01 22:50:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-02 00:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-02 03:25:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-11-02 06:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-02 08:00:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-02 11:50:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-02 14:05:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-11-02 15:10:00+0800'),
            interval_class='waiting for cargo due to rejection'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-02 23:15:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-03 02:55:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-03 05:30:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-03 09:50:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-03 10:50:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-03 13:40:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-03 18:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-03 20:30:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-03 22:25:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=25,
            interval_from=pdt('2019-11-04 00:50:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-04 02:30:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-04 06:15:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-04 09:55:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-04 14:30:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-04 18:45:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=50,
            interval_from=pdt('2019-11-04 20:35:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-05 02:50:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=75,
            interval_from=pdt('2019-11-05 04:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-05 07:45:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-05 15:00:00+0800'),
            interval_class='end'
        )
        detail.save()

        statement._compute()
        statement = LayDaysStatement.objects.get(shipment__name='452-C')
        self.assertAlmostEqual(statement.demurrage,
                               Decimal(275186.98),
                               places=2)
