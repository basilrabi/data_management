from datetime import timedelta
from decimal import Decimal
from django.test import TestCase
from django.utils.dateparse import parse_datetime as pdt

from custom.variables import one_day
from shipment.models.dso import (LayDaysDetail,
                                 LayDaysStatement,
                                 Shipment,
                                 Vessel)

# pylint: disable=no-member

class  LayDaysStatement453CTest(TestCase):

    def setUp(self):
        vessel = Vessel(name='Sheng Heng Hai')
        vessel.save()
        shipment = Shipment(
            name='453-C', vessel=vessel,
            start_loading=pdt('2019-10-18 07:55:00+0800'),
            end_loading=pdt('2019-11-10 14:00:00+0800')
        )
        shipment.save()

    def test_laydays_computation_452c(self):
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
            can_test=18
        )
        statement.save()
        self.assertAlmostEqual(
            statement.time_can_test() / one_day, 0.03125, places=5
        )
        self.assertAlmostEqual(
            statement.time_limit() / one_day,
            timedelta(days=9, hours=5, minutes=9, seconds=0) / one_day,
            places=5
        )

        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-13 12:00:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-10-14 04:30:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-14 05:30:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-10-14 21:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-15 06:00:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-10-15 07:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-15 12:30:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-10-16 02:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-16 05:00:00+0800'),
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
            interval_from=pdt('2019-10-16 12:30:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-10-16 21:45:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-17 06:00:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-10-17 07:00:00+0800'),
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
            interval_from=pdt('2019-10-18 07:50:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-10-18 16:20:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-18 20:30:00+0800'),
            interval_class='waiting for cargo'
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
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-19 22:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-20 03:05:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-20 13:40:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-20 22:15:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-21 00:40:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-21 04:55:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-21 15:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-21 18:55:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-22 01:25:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-10-22 03:45:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-22 07:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-22 22:20:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-23 12:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-24 04:05:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-10-24 06:00:00+0800'),
            interval_class='heavy swell'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-24 07:00:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-24 11:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-24 22:35:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-25 05:30:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-25 15:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-26 14:20:00+0800'),
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
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-28 16:00:00+0800'),
            interval_class='heavy swell'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-28 18:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-10-28 18:05:00+0800'),
            interval_class='waiting for cargo due to rejection'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-28 21:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-10-29 07:00:00+0800'),
            interval_class='waiting for cargo due to rejection'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-10-29 11:36:00+0800'),
            interval_class='continuous loading'
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
            interval_from=pdt('2019-10-31 15:30:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-10-31 15:35:00+0800'),
            interval_class='waiting for cargo due to rejection'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-01 03:20:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-11-01 10:00:00+0800'),
            interval_class='waiting for cargo due to rejection'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-01 12:30:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-11-01 19:30:00+0800'),
            interval_class='waiting for cargo due to rejection'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-01 22:50:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-11-02 00:00:00+0800'),
            interval_class='waiting for cargo due to rejection'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-02 06:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-02 08:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-02 13:25:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-02 17:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-11-02 22:25:00+0800'),
            interval_class='waiting for cargo due to rejection'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-03 05:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-11-03 05:05:00+0800'),
            interval_class='waiting for cargo due to rejection'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-03 12:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-03 19:40:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-04 00:50:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-04 13:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-04 20:50:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-05 08:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-05 20:50:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-06 02:40:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-06 04:55:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-06 07:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-11-06 18:15:00+0800'),
            interval_class='waiting for cargo due to rejection'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-06 21:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-07 05:00:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-07 08:20:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-07 18:15:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-07 19:20:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-08 18:20:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-08 19:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-11-08 22:00:00+0800'),
            interval_class='waiting for cargo due to rejection'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-09 07:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=0,
            interval_from=pdt('2019-11-09 16:05:00+0800'),
            interval_class='waiting for cargo due to rejection'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-09 16:45:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-09 20:25:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-10 00:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-11-10 14:00:00+0800'),
            interval_class='end'
        )
        detail.save()

        statement._compute()
        statement = LayDaysStatement.objects.get(shipment__name='453-C')
        self.assertAlmostEqual(statement.demurrage,
                               Decimal(288423.61),
                               places=2)
