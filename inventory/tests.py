from django.contrib.gis.geos import GEOSGeometry
from django.test import TestCase

from custom.functions import setup_triggers
from inventory.models.insitu import Block

class BlockTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        setup_triggers()

    def setUp(self):
        pass

    def test_exposed_is_set(self):
        block = Block(name='b1', z=99, ni=1, fe=40, co=0.1,
                      geom=GEOSGeometry('SRID=3125;POINT (591100 1051100)'))
        block.save()
        block.refresh_from_db()
        self.assertEqual(None, block.exposed)

        block = Block(name='b2', z=99, ni=1, fe=40, co=0.1, depth = 1,
                      geom=GEOSGeometry('SRID=3125;POINT (591100 1051100)'))
        block.save()
        block.refresh_from_db()
        self.assertEqual(True, block.exposed)

        block = Block(name='b3', z=99, ni=1, fe=40, co=0.1, depth = 0,
                      geom=GEOSGeometry('SRID=3125;POINT (591100 1051100)'))
        block.save()
        block.refresh_from_db()
        self.assertEqual(False, block.exposed)

    def test_exposed_is_updated(self):
        block = Block(name='b1', z=99, ni=1, fe=40, co=0.1,
                      geom=GEOSGeometry('SRID=3125;POINT (591100 1051100)'))
        block.save()
        block.refresh_from_db()
        self.assertEqual(None, block.exposed)

        block.depth = 1
        block.save()
        block.refresh_from_db()
        self.assertEqual(True, block.exposed)

        block.depth = 0
        block.save()
        block.refresh_from_db()
        self.assertEqual(False, block.exposed)
