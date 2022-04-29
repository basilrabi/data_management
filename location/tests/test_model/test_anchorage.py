from django.test import TestCase
from django.utils.dateparse import parse_datetime as pdt

from custom.functions import setup_triggers
from location.models.shipment import Anchorage
from shipment.models.dso import LayDaysStatement, Shipment, Vessel


class AnchorageTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        setup_triggers()

    def setUp(self):
        vessel = Vessel(name='Jin Yuan')
        vessel.save()
        shipment = Shipment(name='540-C', vessel=vessel)
        shipment.save()
        statement = LayDaysStatement(shipment=shipment)
        statement.save()

    def test_geometry_update(self):
        statement = LayDaysStatement.objects.all().first()
        anchor = Anchorage(laydays=statement,
                           anchored=pdt('2021-06-06 13:00:00+0800'),
                           latitude_minutes=34.45,
                           longitude_minutes=48.57)
        anchor.save()
        anchor.refresh_from_db()
        self.assertEqual(anchor.geom.coords[0], 125.8095)
        self.assertEqual(anchor.geom.coords[1], 9 + (34.45 / 60))
