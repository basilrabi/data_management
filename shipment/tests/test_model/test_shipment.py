from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils.dateparse import parse_datetime as pd

from shipment.models.dso import Shipment, Vessel

# pylint: disable=no-member

class  ShipmentTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        vessel = Vessel(name='guagua')
        vessel.save()

    def setUp(self):
        pass

    def test_end_is_valid(self):
        vessel = Vessel.objects.all().first()
        shipment = Shipment(
            name='284', vessel=vessel,
            start_loading='2019-08-17 00:00:00+0800',
            end_loading='2019-08-19 00:00:00+0800'
        )
        self.assertEqual(shipment.clean(), None)
        shipment.save()
        shipment = Shipment.objects.all().first()

        self.assertEqual(shipment.start_loading, pd('2019-08-17 00:00:00+0800'))
        self.assertEqual(shipment.end_loading, pd('2019-08-19 00:00:00+0800'))

    def test_name_is_unique(self):
        vessel = Vessel.objects.all().first()
        shipment = Shipment(
            name='284', vessel=vessel,
            start_loading='2019-08-17 00:00:00+0800',
            end_loading='2019-08-19 00:00:00+0800'
        )
        self.assertEqual(shipment.clean(), None)
        shipment.save()

        shipment = Shipment(
            name='284  ', vessel=vessel,
            start_loading='2019-08-20 00:00:00+0800',
            end_loading='2019-08-25 00:00:00+0800'
        )
        self.assertRaises(IntegrityError, shipment.save)

    def test_shipment_do_not_overlap(self):
        vessel = Vessel.objects.all().first()
        shipment = Shipment(
            name='284', vessel=vessel,
            start_loading='2019-08-17 00:05:00+0800',
            end_loading='2019-08-19 00:05:00+0800'
        )
        shipment.save()

        shipment = Shipment(
            name='285', vessel=vessel,
            start_loading='2019-08-19 00:04:00+0800',
            end_loading='2019-08-21 00:05:00+0800'
        )
        self.assertRaises(ValidationError, shipment.clean)

        shipment = Shipment(
            name='285', vessel=vessel,
            start_loading='2019-08-17 00:05:00+0800',
            end_loading='2019-08-14 00:05:00+0800'
        )
        self.assertRaises(ValidationError, shipment.clean)

        shipment = Shipment(
            name='285', vessel=vessel,
            start_loading='2019-08-20 00:05:00+0800',
            end_loading='2019-08-21 00:05:00+0800'
        )
        self.assertEqual(shipment.clean(), None)

        shipment = Shipment(
            name='285', vessel=vessel,
            start_loading='2019-08-14 00:05:00+0800',
            end_loading='2019-08-16 00:05:00+0800'
        )
        self.assertEqual(shipment.clean(), None)
