from django.contrib.gis.geos import GEOSGeometry
from django.test import TestCase

from custom.functions import setup_triggers
from inventory.models.insitu import Block
from location.models.source import ClippedCluster, Cluster, Slice

slice1 = Slice(
    z=96,
    layer=2,
    geom=GEOSGeometry('SRID=3125;LINESTRING(591095 1051085 96,591095 1051105 96,591105 1051105 96,591105 1051095 96,591115 1051095 96,591115 1051085 96,591095 1051085 96)')
)

slice2 = Slice(
    z=96,
    layer=2,
    geom=GEOSGeometry('SRID=3125;LINESTRING(591106 1051086 96,591106 1051094 96,591114 1051094 96,591114 1051086 96,591106 1051086 96)')
)

class ClippedClusterTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        setup_triggers()

    def setUp(self):
        block = Block(name='b1', z=99, ni=1, fe=40, co=0.1,
                      geom=GEOSGeometry('SRID=3125;POINT (591100 1051100)'))
        block.save()
        block = Block(name='b2', z=99, ni=2, fe=42, co=0.2,
                      geom=GEOSGeometry('SRID=3125;POINT (591110 1051100)'))
        block.save()
        block = Block(name='b3', z=99, ni=1, fe=40, co=0.1,
                      geom=GEOSGeometry('SRID=3125;POINT (591100 1051090)'))
        block.save()
        block = Block(name='b4', z=99, ni=2, fe=40, co=0.1,
                      geom=GEOSGeometry('SRID=3125;POINT (591110 1051090)'))
        block.save()
        cluster = Cluster(name='c1')
        cluster.save()

    def test_update_on_block_update(self):
        cluster = Cluster.objects.get(name='c1')
        block = Block.objects.get(name='b1')
        block.cluster = cluster
        block.save()
        cluster.refresh_from_db()
        clipped_cluster = ClippedCluster.objects.get(name=cluster.name)
        self.assertEqual(clipped_cluster.ni, 1)
        self.assertEqual(clipped_cluster.fe, 40)
        self.assertEqual(clipped_cluster.co, 0.1)

        # Update block
        block.ni = 2
        block.fe = 45
        block.co = 0.05
        block.save()
        clipped_cluster.refresh_from_db()
        self.assertEqual(clipped_cluster.ni, 2)
        self.assertEqual(clipped_cluster.fe, 45)
        self.assertEqual(clipped_cluster.co, 0.05)

    def test_update_on_cluster_update(self):
        # 1 block assigned
        cluster = Cluster.objects.get(name='c1')
        block = Block.objects.get(name='b1')
        block.cluster = cluster
        block.save()
        cluster.refresh_from_db()
        clipped_cluster = ClippedCluster.objects.get(name=cluster.name)
        self.assertEqual(clipped_cluster.geom.area, 100)
        self.assertEqual(clipped_cluster.ni, 1)

        # 2 blocks assgined
        block = Block.objects.get(name='b2')
        block.cluster = cluster
        block.save()
        clipped_cluster.refresh_from_db()
        self.assertEqual(clipped_cluster.geom.area, 200)
        self.assertEqual(clipped_cluster.ni, 1.5)

        # 1 block removed
        block = Block.objects.get(name='b2')
        block.cluster = None
        block.save()
        clipped_cluster.refresh_from_db()
        self.assertEqual(clipped_cluster.geom.area, 100)
        self.assertEqual(clipped_cluster.ni, 1)

    def test_update_on_slice_add_and_remove(self):
        cluster = Cluster.objects.get(name='c1')
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
        cluster.refresh_from_db()

        # No slice
        clipped_cluster = ClippedCluster.objects.get(name=cluster.name)
        self.assertEqual(clipped_cluster.geom.area, 400)
        self.assertEqual(clipped_cluster.ni, 1.5)

        # With slice
        slice1.save()
        clipped_cluster.refresh_from_db()
        self.assertEqual(clipped_cluster.geom.area, 300)
        self.assertEqual(clipped_cluster.ni, 1.33)

        # With internal ring
        slice2.save()
        clipped_cluster.refresh_from_db()
        self.assertEqual(clipped_cluster.geom.area, 236)
        self.assertEqual(clipped_cluster.ni, 1.15)

        # Remove external ring
        slice = Slice.objects.get(geom__equals=slice1.geom)
        slice.delete()
        clipped_cluster.refresh_from_db()
        self.assertEqual(clipped_cluster.geom.area, 64)
        self.assertEqual(clipped_cluster.ni, 2)

        # No Slice
        slice = Slice.objects.get(geom__equals=slice2.geom)
        slice.delete()
        clipped_cluster.refresh_from_db()
        self.assertEqual(clipped_cluster.geom.area, 400)
        self.assertEqual(clipped_cluster.ni, 1.5)
