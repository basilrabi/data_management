from django.test import TestCase
from django.contrib.gis.geos import LineString
from django.db.utils import IntegrityError, InternalError

from custom.functions import setup_triggers
from location.models.source import Slice

# pylint: disable=no-member

crest_line = LineString((593970, 1051940, 100),
                        (593970, 1051950, 110),
                        (593980, 1051950, 110),
                        (593980, 1051940, 100),
                        (593970, 1051940, 100), srid=3125)
open_string = LineString((593970, 1051940, 100),
                         (593970, 1051950, 110),
                         (593980, 1051950, 110),
                         (593980, 1051940, 110),
                         (593970, 1051940, 110), srid=3125)
toe_line = LineString((593980, 1051940, 100),
                      (593970, 1051940, 100), srid=3125)
road_line = LineString((593970, 1051940, 100),
                       (593970, 1051950, 110), srid=3125)


class SliceTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        setup_triggers()

    def setUp(self):
        pass

    def test_valid_inputs(self):
        slice1 = Slice(z=100, layer=2, geom=crest_line)
        self.assertEqual(slice1.save(), None)
        slice1 = Slice(z=100, layer=7, geom=road_line)
        self.assertEqual(slice1.save(), None)
        slice1 = Slice(z=100, layer=8, geom=toe_line)
        self.assertEqual(slice1.save(), None)

    def test_invalid_crest_line(self):
        slice1 = Slice(z=100, layer=2, geom=open_string)
        self.assertRaises(IntegrityError, slice1.save)

    def test_invalid_other_line(self):
        slice1 = Slice(z=100, layer=3, geom=open_string)
        self.assertRaises(IntegrityError, slice1.save)

    def test_overlap(self):
        slice1 = Slice(z=100, layer=2, geom=crest_line)
        slice1.save()
        slice2 = Slice(z=100, layer=2, geom=crest_line)
        self.assertRaises(InternalError, slice2.save)
