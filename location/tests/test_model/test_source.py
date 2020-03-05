from django.db import connection
from django.contrib.gis.geos import GEOSGeometry
from django.db.utils import IntegrityError
from django.test import TestCase

from location.models.source import MineBlock, Stockyard, DrillHole

# pylint: disable=no-member

class DrillHoleTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        with open('scripts/sql/trigger/location_drillhole_update.pgsql', 'r') as file:
            query = file.read()
            with connection.cursor() as cursor:
                cursor.execute(query)

    def setUp(self):
        drillhole = DrillHole(name='MyHole')
        drillhole.save()

    def test_auto_geom_update(self):
        drillhole = DrillHole.objects.all().first()
        drillhole.x = 591070
        drillhole.save()

        drillhole = DrillHole.objects.all().first()
        self.assertEqual(drillhole.geom, None)

        drillhole.y = 1051100
        drillhole.save()

        drillhole = DrillHole.objects.all().first()
        self.assertEqual(drillhole.geom, GEOSGeometry('SRID=3125;POINT (591070 1051100)'))

class MineBlockTest(TestCase):

    def setUp(self):
        pass

    def test_name_is_unique_part1(self):
        mb = MineBlock(ridge='T1', name='MB 201-A')
        mb.save()
        mb = MineBlock(ridge='T1', name='MB 201A')
        self.assertRaises(IntegrityError, mb.save)

    def test_name_is_unique_per_ridge_part_2(self):
        mb = MineBlock(ridge='T1', name='MB 201-A')
        mb.save()
        mb = MineBlock(ridge='T2', name='201 A')
        self.assertRaises(IntegrityError, mb.save)

    def test_name_is_unique_per_ridge_part_3(self):
        mb = MineBlock(ridge='T1', name='MB 201-A')
        mb.save()
        mb = MineBlock(ridge='T2', name='1 A')
        self.assertEqual(None, mb.save())

class StockyardTest(TestCase):

    def setUp(self):
        pass

    def test_name_is_unique_per_ridge_part(self):
        yard = Stockyard(name='LDA 1')
        yard.save()
        yard = Stockyard(name='LDA-1')
        self.assertRaises(IntegrityError, yard.save)
