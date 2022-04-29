from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils.dateparse import parse_datetime as pdt

from custom.functions import setup_triggers
from shipment.models.dso import (
    LayDaysDetail,
    LayDaysStatement,
    Shipment,
    Vessel
)


class  LayDaysDetailTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        setup_triggers()

    def setUp(self):
        vessel = Vessel(name='guagua')
        vessel.save()
        shipment = Shipment(name='284', vessel=vessel)
        shipment.save()
        statement = LayDaysStatement(
            shipment=shipment,
            arrival_pilot=pdt('2019-08-16 00:00:00+0800'),
            arrival_tmc=pdt('2019-08-16 12:00:00+0800')
        )
        statement.save()

    def test_only_one_end_per_statement(self):
        statement = LayDaysStatement.objects.all().first()
        detail = LayDaysDetail(
            laydays=statement,
            interval_from=pdt('2019-08-17 12:00:00+0800'),
            laytime_rate=100,
            interval_class='end'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement,
            interval_from=pdt('2019-08-17 12:05:00+0800'),
            laytime_rate=100,
            interval_class='end'
        )
        self.assertRaises(IntegrityError, detail.save)

    def test_unique_interval_from_integrity(self):
        statement = LayDaysStatement.objects.all().first()
        detail = LayDaysDetail(
            laydays=statement,
            interval_from=pdt('2019-08-17 12:00:00+0800'),
            laytime_rate=100,
            interval_class='rain'
        )
        detail.save()
        detail = LayDaysDetail(
            laydays=statement,
            interval_from=pdt('2019-08-17 12:00:00+0800'),
            laytime_rate=100,
            interval_class='heavy swell'
        )
        self.assertRaises(IntegrityError, detail.save)
