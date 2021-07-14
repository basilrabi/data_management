from django.contrib.gis.geos import GEOSGeometry
from django.test import TestCase

from custom.functions import setup_triggers
from location.models.source import DrillHole

# pylint: disable=no-member


class DrillHoleTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        setup_triggers()

    def setUp(self):
        drillhole = DrillHole(name='MyHole')
        drillhole.save()

    def test_auto_geom_creation(self):
        drillhole = DrillHole(name='MyOtherHole',
                              x=591070,
                              y=1051100)
        drillhole.save()

        drillhole = DrillHole.objects.get(name='MyOtherHole')
        self.assertEqual(drillhole.geom,
                         GEOSGeometry('SRID=3125;POINT (591070 1051100)'))

    def test_auto_geom_update(self):
        drillhole = DrillHole.objects.all().first()
        drillhole.x = 591070
        drillhole.save()

        drillhole = DrillHole.objects.all().first()
        self.assertEqual(drillhole.geom, None)

        drillhole.y = 1051100
        drillhole.save()

        drillhole = DrillHole.objects.all().first()
        self.assertEqual(drillhole.geom,
                         GEOSGeometry('SRID=3125;POINT (591070 1051100)'))
