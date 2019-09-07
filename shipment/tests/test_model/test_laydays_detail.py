from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.dateparse import parse_datetime as pdt

from shipment.models.dso import (LayDaysDetail,
                                 LayDaysStatement,
                                 Shipment,
                                 Vessel)

class  LayDaysDetailTest(TestCase):

    def setUp(self):
        vessel = Vessel(name='guagua')
        vessel.save()
        shipment = Shipment(
            name='284', vessel=vessel,
            start_loading=pdt('2019-08-17 00:00:00+0800'),
            end_loading=pdt('2019-08-19 00:00:00+0800')
        )
        shipment.save()
        statement = LayDaysStatement(
            shipment=shipment,
            arrival_pilot=pdt('2019-08-16 00:00:00+0800'),
            arrival_tmc=pdt('2019-08-16 12:00:00+0800')
        )
        statement.save()

    def test_loading_rate_does_not_exceed_100(self):
        # pylint: disable=E1101
        statement = LayDaysStatement.objects.all().first()
        detail = LayDaysDetail(
            laydays=statement,
            interval_from=pdt('2019-08-17 12:00:00+0800'),
            loading_rate=101,
            interval_class='waiting_for_cargo'
        )
        self.assertRaises(ValidationError, detail.clean)

    def test_only_one_end_per_statement(self):
        # pylint: disable=E1101
        statement = LayDaysStatement.objects.all().first()
        detail = LayDaysDetail(
            laydays=statement,
            interval_from=pdt('2019-08-17 12:00:00+0800'),
            loading_rate=100,
            interval_class='end'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement,
            interval_from=pdt('2019-08-17 12:05:00+0800'),
            loading_rate=100,
            interval_class='end'
        )
        self.assertRaises(ValidationError, detail.clean)

    def test_unique_interval_from(self):
        # pylint: disable=E1101
        statement = LayDaysStatement.objects.all().first()
        detail = LayDaysDetail(
            laydays=statement,
            interval_from=pdt('2019-08-17 12:00:00+0800'),
            loading_rate=100,
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement,
            interval_from=pdt('2019-08-17 12:00:00+0800'),
            loading_rate=100,
            interval_class='swell'
        )
        self.assertRaises(ValidationError, detail.clean)
