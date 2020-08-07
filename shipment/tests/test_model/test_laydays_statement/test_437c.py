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

class  LayDaysStatement437CTest(TestCase):

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
        self.assertAlmostEqual(
            statement.time_limit(), timedelta(days=9, hours=13, minutes=48)
        )

        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-08-29 08:40:00+0800'),
            interval_class='waiting for loading commencement'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-08-30 22:10:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-08-31 05:30:00+0800'),
            interval_class='waiting for loading commencement'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-01 02:10:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-01 05:20:00+0800'),
            interval_class='waiting for loading commencement'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-01 07:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-01 11:10:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-01 20:20:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-01 23:30:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-02 00:35:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-02 12:55:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-02 17:30:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-02 19:30:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-02 20:40:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-03 04:20:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-03 10:20:00+0800'),
            interval_class='heavy swell'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-03 13:40:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-03 22:20:00+0800'),
            interval_class='heavy swell'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-04 00:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-04 01:00:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-04 03:30:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-04 07:40:00+0800'),
            interval_class='heavy swell'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-04 09:50:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-04 13:15:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-04 16:25:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-04 21:15:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-04 23:50:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-05 02:20:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-05 03:45:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-05 10:50:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-05 11:05:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-05 13:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-05 13:25:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-05 22:10:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-06 01:15:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-06 03:20:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-06 10:25:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-06 21:20:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-07 02:10:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-07 06:10:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-07 11:30:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-07 19:40:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-07 23:30:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-08 00:45:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-08 02:15:00+0800'),
            interval_class='heavy swell'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-08 03:50:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-08 09:10:00+0800'),
            interval_class='heavy swell'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-08 12:40:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-08 14:40:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-08 17:50:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-08 22:25:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-09 01:30:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-09 07:00:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-09 17:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-09 18:30:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-09 21:40:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-10 02:30:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-10 04:10:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-10 09:00:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-10 13:30:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-10 22:20:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-11 02:30:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-11 08:40:00+0800'),
            interval_class='heavy swell'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-11 12:45:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-11 13:10:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-11 19:50:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-12 12:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-12 13:10:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-12 17:20:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-12 19:23:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-13 00:30:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-13 04:55:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-13 08:20:00+0800'),
            interval_class='heavy swell'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-13 10:30:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-13 11:00:00+0800'),
            interval_class='heavy swell'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-13 13:50:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-13 17:00:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-13 19:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-13 20:15:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-13 23:30:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-14 10:20:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-14 11:00:00+0800'),
            interval_class='heavy swell'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-14 14:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-14 15:50:00+0800'),
            interval_class='heavy swell'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-14 19:40:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-14 23:50:00+0800'),
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-15 02:50:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-15 03:20:00+0800'),
            interval_class='heavy swell'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-15 05:30:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-15 08:30:00+0800'),
            interval_class='heavy swell'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-15 11:00:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-15 14:40:00+0800'),
            interval_class='waiting for cargo'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-15 17:30:00+0800'),
            interval_class='continuous loading'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement, laytime_rate=100,
            interval_from=pdt('2019-09-16 05:00:00+0800'),
            interval_class='end'
        )
        detail.save()

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
