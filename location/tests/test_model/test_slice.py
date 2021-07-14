from django.test import TestCase
from django.contrib.gis.geos import GEOSGeometry, LineString
from django.db.utils import IntegrityError, InternalError

from custom.functions import setup_triggers
from inventory.models.insitu import Block
from location.models.source import Cluster, ClusterLayout, Crest, Slice

# pylint: disable=no-member

crest_line = LineString(
    (593970, 1051940, 100),
    (593970, 1051950, 110),
    (593980, 1051950, 110),
    (593980, 1051940, 100),
    (593970, 1051940, 100),
    srid=3125
)
crest_line_external = LineString(
    (593990, 1051960, 100),
    (593990, 1051970, 110),
    (594000, 1051970, 110),
    (594000, 1051960, 100),
    (593990, 1051960, 100),
    srid=3125
)
crest_line_internal = LineString(
    (593974, 1051944, 100),
    (593974, 1051946, 110),
    (593976, 1051946, 110),
    (593976, 1051944, 100),
    (593974, 1051944, 100),
    srid=3125
)
crest_line_internal_double = LineString(
    (593974.5, 1051944.5, 100),
    (593974.5, 1051945.5, 110),
    (593975.5, 1051945.5, 110),
    (593975.5, 1051944.5, 100),
    (593974.5, 1051944.5, 100),
    srid=3125
)
crest_line_internal_touch = LineString(
    (593970, 1051940, 100),
    (593970, 1051942, 110),
    (593972, 1051942, 110),
    (593972, 1051940, 100),
    (593970, 1051940, 100),
    srid=3125
)
crest_line_partial = LineString(
    (593979, 1051949, 100),
    (593979, 1051951, 110),
    (593981, 1051951, 110),
    (593981, 1051949, 100),
    (593979, 1051949, 100),
    srid=3125
)
open_string = LineString(
    (593970, 1051940, 100),
    (593970, 1051950, 110),
    (593980, 1051950, 110),
    (593980, 1051940, 110),
    (593970, 1051940, 110),
    srid=3125
)
toe_line = LineString(
    (593980, 1051940, 100),
    (593970, 1051940, 100),
    srid=3125
)
road_line = LineString(
    (593970, 1051940, 100),
    (593970, 1051950, 110),
    srid=3125
)


class SliceTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        setup_triggers()

    def setUp(self):
        pass

    def test_blocked_removal_when_surveyed(self):
        slice_geom = GEOSGeometry('SRID=3125;LINESTRING(591095 1051085 96, 591095 1051105 96, 591105 1051105 96, 591105 1051095 96, 591115 1051095 96, 591115 1051085 96, 591095 1051085 96)')
        block = Block(name='b1', z=99, ni=1, fe=40, co=0.1,
                      geom=GEOSGeometry('SRID=3125;POINT (591100 1051100)'))
        block.save()
        block = Block(name='b2', z=99, ni=2, fe=42, co=0.2,
                      geom=GEOSGeometry('SRID=3125;POINT (591110 1051100)'))
        block.save()
        block = Block(name='b3', z=99, ni=1, fe=40, co=0.1,
                      geom=GEOSGeometry('SRID=3125;POINT (591100 1051090)'))
        block.save()
        block = Block(name='b4', z=99, ni=1, fe=40, co=0.1,
                      geom=GEOSGeometry('SRID=3125;POINT (591110 1051090)'))
        block.save()
        cluster = Cluster(name='c1')
        cluster.save()
        cluster.refresh_from_db()
        block = Block.objects.get(name='b1')
        block.cluster = cluster
        block.save()
        block = Block.objects.get(name='b2')
        block.cluster = cluster
        block.save()
        block = Block.objects.get(name='b3')
        block.cluster = cluster
        block.save()
        block = Block.objects.get(name='b4')
        block.cluster = cluster
        block.save()
        slice = Slice(z=96, layer=2, geom=slice_geom)
        slice.save()
        cluster.refresh_from_db()
        cluster.date_scheduled = '2020-05-30'
        cluster.save()
        layout = ClusterLayout(cluster=cluster, layout_date='2020-05-30')
        layout.save()
        slice = Slice.objects.get(z=96, layer=2, geom__equals=slice_geom)
        self.assertRaises(InternalError, slice.delete)

    def test_valid_inputs(self):
        slice1 = Slice(z=100, layer=2, geom=crest_line)
        self.assertEqual(slice1.save(), None)
        slice1 = Slice(z=100, layer=7, geom=road_line)
        self.assertEqual(slice1.save(), None)
        slice1 = Slice(z=100, layer=8, geom=toe_line)
        self.assertEqual(slice1.save(), None)
        slice1 = Slice(z=100, layer=2, geom=crest_line_external)
        self.assertEqual(slice1.save(), None)

    def test_invalid_crest_line(self):
        slice1 = Slice(z=100, layer=2, geom=open_string)
        self.assertRaises(IntegrityError, slice1.save)

    def test_invalid_other_line(self):
        slice1 = Slice(z=100, layer=3, geom=open_string)
        self.assertRaises(IntegrityError, slice1.save)

    def test_invalid_overlap_exact(self):
        slice1 = Slice(z=100, layer=2, geom=crest_line)
        slice1.save()
        slice2 = Slice(z=100, layer=2, geom=crest_line)
        self.assertRaises(InternalError, slice2.save)

    def test_invalid_triple_ring_between(self):
        slice3 = Slice(z=100, layer=2, geom=crest_line_internal_double)
        slice3.save()
        slice1 = Slice(z=100, layer=2, geom=crest_line)
        slice1.save()
        slice2 = Slice(z=100, layer=2, geom=crest_line_internal)
        self.assertRaises(InternalError, slice2.save)

    def test_invalid_triple_ring_expanding(self):
        slice3 = Slice(z=100, layer=2, geom=crest_line_internal_double)
        slice3.save()
        slice2 = Slice(z=100, layer=2, geom=crest_line_internal)
        slice2.save()
        slice1 = Slice(z=100, layer=2, geom=crest_line)
        self.assertRaises(InternalError, slice1.save)

    def test_invalid_triple_ring_shrinking(self):
        slice1 = Slice(z=100, layer=2, geom=crest_line)
        slice1.save()
        slice2 = Slice(z=100, layer=2, geom=crest_line_internal)
        slice2.save()
        slice3 = Slice(z=100, layer=2, geom=crest_line_internal_double)
        self.assertRaises(InternalError, slice3.save)

    def test_overlap_internal(self):
        slice1 = Slice(z=100, layer=2, geom=crest_line)
        slice1.save()
        slice2 = Slice(z=100, layer=2, geom=crest_line_internal)
        slice2.save()
        crest = Crest.objects.get(z=slice2.z, geom__bboverlaps=slice2.geom)
        self.assertEqual(crest.geom.area, 100 - 4)

    def test_overlap_internal_touch(self):
        slice1 = Slice(z=100, layer=2, geom=crest_line)
        slice1.save()
        slice2 = Slice(z=100, layer=2, geom=crest_line_internal_touch)
        self.assertRaises(InternalError, slice2.save)

    def test_overlap_partial(self):
        slice1 = Slice(z=100, layer=2, geom=crest_line)
        slice1.save()
        slice2 = Slice(z=100, layer=2, geom=crest_line_partial)
        self.assertRaises(InternalError, slice2.save)
