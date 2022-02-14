from django.contrib.gis.geos import GEOSGeometry
from django.db.utils import InternalError
from django.test import TestCase
from django.utils.dateparse import parse_date as pd

from custom.functions import setup_triggers
from inventory.models.insitu import Block
from location.models.landuse import RoadArea
from location.models.source import Cluster, ClusterLayout

# pylint: disable=no-member


class ClusterTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        setup_triggers()

    def setUp(self):
        block = Block(name='b1',
                      z=99,
                      ni=1,
                      fe=40,
                      co=0.1,
                      geom=GEOSGeometry('SRID=3125;POINT (591100 1051100)'))
        block.save()
        block = Block(name='b2',
                      z=99,
                      ni=2,
                      fe=42,
                      co=0.2,
                      geom=GEOSGeometry('SRID=3125;POINT (591110 1051100)'))
        block.save()
        block = Block(name='b3',
                      z=102,
                      ni=2,
                      fe=42,
                      co=0.2,
                      geom=GEOSGeometry('SRID=3125;POINT (591100 1051100)'))
        block.save()
        block = Block(name='b4',
                      z=99,
                      ni=1,
                      fe=40,
                      co=0.1,
                      geom=GEOSGeometry('SRID=3125;POINT (591100 1051090)'))
        block.save()
        block = Block(name='b5',
                      z=99,
                      ni=1,
                      fe=40,
                      co=0.1,
                      geom=GEOSGeometry('SRID=3125;POINT (591110 1051090)'))
        block.save()
        block = Block(name='T1-02-02030-S',
                      z=114,
                      ni=1.55,
                      fe=13.28,
                      co=0.02,
                      geom=GEOSGeometry('SRID=3125;POINT (588455 1054115)'))
        block.save()
        block = Block(name='T1-02-02031-S',
                      z=114,
                      ni=1.46,
                      fe=11.53,
                      co=0.02,
                      geom=GEOSGeometry('SRID=3125;POINT (588465 1054115)'))
        block.save()
        road = RoadArea(
            date_surveyed='2020-03-06',
            geom=GEOSGeometry('SRID=3125;MULTIPOLYGON (((591115 1051105, 591125 1051105, 591125 1051095, 591115 1051095, 591115 1051105)))')
        )
        road.save()
        cluster = Cluster(name='c1')
        cluster.save()

    def test_correct_computation(self):
        cluster = Cluster.objects.get(name='c1')
        road = RoadArea.objects.all().first()

        # No assigned blocks
        self.assertEqual(cluster.geom, None)
        self.assertEqual(cluster.mine_block, None)

        block = Block.objects.get(name='b1')
        block.cluster = cluster
        block.save()

        # 1 block assigned with grade lower than 1.45
        cluster = Cluster.objects.get(name='L1-099-104')
        self.assertEqual(cluster.geom.area, 100)
        self.assertEqual(cluster.ni, 1)
        self.assertEqual(cluster.fe, 40)
        self.assertEqual(cluster.co, 0.1)

        block = Block.objects.get(name='b2')
        block.cluster = cluster
        block.save()

        # 2 blocks assigned with grade of 1.5
        cluster = Cluster.objects.get(name='F1-099-104')
        self.assertEqual(cluster.geom.area, 200)
        self.assertEqual(cluster.ni, 1.5)
        self.assertEqual(cluster.fe, 41)
        self.assertEqual(cluster.co, 0.15)

        cluster.road = road
        cluster.save()

        # Road assigned without buffer
        cluster = Cluster.objects.get(name='F1-099-104')
        self.assertEqual(cluster.geom.area, 200)
        self.assertEqual(cluster.ni, 1.5)
        self.assertEqual(cluster.fe, 41)
        self.assertEqual(cluster.co, 0.15)

        cluster.distance_from_road = 5
        cluster.save()

        # Road assigned with buffer
        cluster = Cluster.objects.get(name='L1-099-104')
        self.assertEqual(cluster.geom.area, 150)
        self.assertEqual(cluster.ni, 1.33)
        self.assertEqual(cluster.fe, 40.67)
        self.assertEqual(cluster.co, 0.13)

    def test_correct_computation_even_with_no_mineblocks(self):
        cluster = Cluster.objects.get(name='c1')
        b1 = Block.objects.get(name='T1-02-02030-S')
        b1.cluster = cluster
        b1.save()
        b2 = Block.objects.get(name='T1-02-02031-S')
        b2.cluster = cluster
        b2.save()
        cluster.refresh_from_db()
        self.assertEqual(cluster.geom.area, 200)
        self.assertEqual(cluster.ni, 1.51)
        self.assertEqual(cluster.fe, 12.41)
        self.assertEqual(cluster.co, 0.02)
        self.assertEqual(cluster.name, 'F1-114-202')

    def test_excavated_and_exposed_are_set(self):
        b4 = Block.objects.get(name='b4')
        b5 = Block.objects.get(name='b5')
        cluster = Cluster.objects.get(name='c1')

        # All blocks not excavated
        b4.depth = 1
        b4.cluster = cluster
        b4.save()
        b5.depth = 1
        b5.cluster = cluster
        b5.save()
        cluster.refresh_from_db()
        self.assertEqual(False, cluster.excavated)
        self.assertEqual(0, cluster.excavation_rate)
        self.assertEqual(100, cluster.exposure_rate)

        b4.cluster = None
        b4.save()
        b5.cluster = None
        b5.save()

        # Blocks partially excavated
        b4.depth = -1
        b4.cluster = cluster
        b4.save()
        b5.cluster = cluster
        b5.save()
        cluster.refresh_from_db()
        self.assertEqual(50, cluster.excavation_rate)
        self.assertEqual(100, cluster.exposure_rate)
        self.assertEqual(False, cluster.excavated)

        b4.cluster = None
        b4.save()
        b5.cluster = None
        b5.save()

        # Blocks fully excavated
        b4.cluster = cluster
        b4.save()
        b5.depth = -1
        b5.cluster = cluster
        b5.save()
        cluster.refresh_from_db()
        self.assertEqual(True, cluster.excavated)
        self.assertEqual(100, cluster.exposure_rate)
        self.assertEqual(100, cluster.excavation_rate)

    def test_excavated_is_set_on_update(self):
        b4 = Block.objects.get(name='b4')
        b5 = Block.objects.get(name='b5')
        cluster = Cluster.objects.get(name='c1')

        # All blocks not excavated
        b4.depth = 4
        b4.cluster = cluster
        b4.save()
        b5.depth = 1
        b5.cluster = cluster
        b5.save()
        cluster.refresh_from_db()
        self.assertEqual(False, cluster.excavated)
        self.assertEqual(0, cluster.excavation_rate)
        self.assertEqual(50, cluster.exposure_rate)

        # Blocks partially excavated
        b4.depth = -1
        b4.save()
        cluster.refresh_from_db()
        self.assertEqual(False, cluster.excavated)
        self.assertEqual(50, cluster.excavation_rate)
        self.assertEqual(100, cluster.exposure_rate)

        # Blocks fully excavated
        b5.depth = -1
        b5.save()
        cluster.refresh_from_db()
        self.assertEqual(True, cluster.excavated)
        self.assertEqual(100, cluster.excavation_rate)
        self.assertEqual(100, cluster.exposure_rate)

        # Blocks editted
        b5.depth = 5
        b5.save()
        cluster.refresh_from_db()
        self.assertEqual(False, cluster.excavated)
        self.assertEqual(50, cluster.excavation_rate)
        self.assertEqual(50, cluster.exposure_rate)

    def test_date_scheduled_lock_if_no_geom(self):
        cluster = Cluster.objects.get(name='c1')
        cluster.date_scheduled = '2020-05-30'
        self.assertRaises(InternalError, cluster.save)

    def test_deletion_of_inventory_block(self):
        cluster = Cluster.objects.get(name='c1')
        block = Block.objects.get(name='b1')
        block.cluster = cluster
        block.save()
        block = Block.objects.get(name='b2')
        block.cluster = cluster
        block.save()

        # Delete 1 block
        block.delete()
        cluster.refresh_from_db()

        self.assertEqual(cluster.geom.area, 100)
        self.assertEqual(cluster.ni, 1)
        self.assertEqual(cluster.fe, 40)
        self.assertEqual(cluster.co, 0.1)

        # Delete another block
        block = Block.objects.get(name='b1')
        block.delete()
        cluster.refresh_from_db()

        self.assertEqual(cluster.geom, None)
        self.assertEqual(cluster.name, '111')
        self.assertEqual(cluster.ni, 0)

    def test_geom_lock_if_date_scheduled(self):
        cluster = Cluster.objects.get(name='c1')
        block = Block.objects.get(name='b1')
        block.cluster = cluster
        block.save()
        cluster.refresh_from_db()
        cluster.date_scheduled = '2020-05-30'
        cluster.save()
        block = Block.objects.get(name='b2')
        block.cluster = cluster
        self.assertRaises(InternalError, block.save)

    def test_invalid_cluster_if_different_elevation(self):
        cluster = Cluster.objects.get(name='c1')

        block = Block.objects.get(name='b1')
        block.cluster = cluster
        block.save()
        block = Block.objects.get(name='b2')
        block.cluster = cluster
        block.save()
        block = Block.objects.get(name='b3')
        block.cluster = cluster
        self.assertRaises(InternalError, block.save)

    def test_layout_date_lock_if_no_schedule(self):
        cluster = Cluster.objects.get(name='c1')
        block = Block.objects.get(name='b1')
        block.cluster = cluster
        block.save()
        layout = ClusterLayout(cluster=cluster, layout_date='2020-05-30')
        self.assertRaises(InternalError, layout.save)

    def test_layout_date_null_lock_if_excavated(self):
        cluster = Cluster.objects.get(name='c1')
        block = Block.objects.get(name='b1')
        block.cluster = cluster
        block.save()
        cluster.date_scheduled = '2020-05-30'
        cluster.save()
        layout = ClusterLayout(cluster=cluster, layout_date='2020-05-30')
        layout.save()
        cluster.excavated = True
        cluster.save()
        self.assertRaises(InternalError, layout.delete)

    def test_layout_date_is_updated(self):
        cluster = Cluster.objects.get(name='c1')
        block = Block.objects.get(name='b1')
        block.cluster = cluster
        block.save()
        cluster.date_scheduled = '2020-05-30'
        cluster.save()
        layout = ClusterLayout(cluster=cluster, layout_date='2020-05-30')
        layout.save()
        cluster.refresh_from_db()
        self.assertEqual(cluster.latest_layout_date, pd('2020-05-30'))
        layout.layout_date = '2020-06-01'
        layout.save()
        cluster.refresh_from_db()
        self.assertEqual(cluster.latest_layout_date, pd('2020-06-01'))
        layout = ClusterLayout(cluster=cluster, layout_date='2020-06-30')
        layout.save()
        cluster.refresh_from_db()
        self.assertEqual(cluster.latest_layout_date, pd('2020-06-30'))
        layout.delete()
        layout = ClusterLayout.objects.get(layout_date=pd('2020-06-01'))
        layout.delete()
        cluster.refresh_from_db()
        self.assertEqual(cluster.latest_layout_date, None)

    def test_layout_date_not_earlier_than_latest(self):
        cluster = Cluster.objects.get(name='c1')
        block = Block.objects.get(name='b1')
        block.cluster = cluster
        block.save()
        cluster.date_scheduled = '2020-05-30'
        cluster.save()
        layout = ClusterLayout(cluster=cluster, layout_date='2020-05-30')
        layout.save()
        layout = ClusterLayout(cluster=cluster, layout_date='2020-04-30')
        self.assertRaises(InternalError, layout.save)

    def test_name_is_reused(self):
        cluster = Cluster.objects.get(name='c1')

        b1 = Block.objects.get(name='b1')
        b1.cluster = cluster
        b1.save()
        b1.refresh_from_db()
        self.assertEqual(b1.cluster.name, 'L1-099-104')

        cluster = Cluster.objects.get(name='111')
        b4 = Block.objects.get(name='b4')
        b4.cluster = cluster
        b4.save()
        b4.refresh_from_db()
        self.assertEqual(b4.cluster.name, 'L2-099-104')

        b1.cluster = None
        b1.save()

        cluster = Cluster.objects.filter(name='111')[0]
        b5 = Block.objects.get(name='b5')
        b5.cluster = cluster
        b5.save()
        b5.refresh_from_db()
        self.assertEqual(b5.cluster.name, 'L1-099-104')

    def test_removal_of_cluster(self):
        cluster = Cluster.objects.get(name='c1')
        block = Block.objects.get(name='b1')
        block.cluster = cluster
        block.save()
        block = Block.objects.get(name='b2')
        block.cluster = cluster
        block.save()

        # With cluster
        cluster = Cluster.objects.get(name='F1-099-104')
        self.assertEqual(cluster.geom.area, 200)
        self.assertEqual(cluster.ni, 1.5)
        self.assertEqual(cluster.fe, 41)
        self.assertEqual(cluster.co, 0.15)

        block = Block.objects.get(name='b1')
        block.cluster = None
        block.save()
        block = Block.objects.get(name='b2')
        block.cluster = None
        block.save()

        # Without cluster
        clusters = Cluster.objects.all().filter(name='111')
        self.assertEqual(clusters.count(), 2)

        cluster = clusters[0]
        self.assertEqual(cluster.geom, None)
        self.assertEqual(cluster.mine_block, None)
        self.assertEqual(cluster.ni, 0)
        self.assertEqual(cluster.fe, 0)
        self.assertEqual(cluster.co, 0)

        cluster = clusters[1]
        self.assertEqual(cluster.geom, None)
        self.assertEqual(cluster.mine_block, None)
        self.assertEqual(cluster.ni, 0)
        self.assertEqual(cluster.fe, 0)
        self.assertEqual(cluster.co, 0)

    def test_updating_block_updates_cluster(self):
        cluster = Cluster.objects.get(name='c1')
        block = Block.objects.get(name='b2')
        block.cluster = cluster
        block.save()
        cluster = Cluster.objects.get(name='111')
        block = Block.objects.get(name='b1')
        block.cluster = cluster
        block.save()
        cluster.refresh_from_db()
        self.assertEqual(cluster.ni, 1)
        self.assertEqual(cluster.fe, 40)
        self.assertEqual(cluster.co, 0.1)

        # Update block
        block.ni = 2
        block.fe = 45
        block.co = 0.05
        block.save()
        cluster.refresh_from_db()
        self.assertEqual(cluster.ni, 2)
        self.assertEqual(cluster.fe, 45)
        self.assertEqual(cluster.co, 0.05)
