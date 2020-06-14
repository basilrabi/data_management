from django.db import connection
from django.contrib.gis.geos import GEOSGeometry
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError, InternalError
from django.test import TestCase

from inventory.models.insitu import Block
from location.models.landuse import RoadArea
from location.models.source import Cluster, DrillHole, MineBlock, Stockyard

# pylint: disable=no-member

class ClusterTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        with open('scripts/sql/function/get_ore_class.pgsql', 'r') as file:
            query = file.read()
            with connection.cursor() as cursor:
                cursor.execute(query)
        with open('scripts/sql/function/insert_dummy_cluster.pgsql', 'r') as file:
            query = file.read()
            with connection.cursor() as cursor:
                cursor.execute(query)
        with open('scripts/sql/lock/location_cluster.pgsql', 'r') as file:
            query = file.read()
            with connection.cursor() as cursor:
                cursor.execute(query)
        with open('scripts/sql/trigger/location_cluster_update.pgsql', 'r') as file:
            query = file.read()
            with connection.cursor() as cursor:
                cursor.execute(query)
        with open('scripts/sql/dump/location_mineblock.pgsql', 'r') as file:
            query = file.read()
            with connection.cursor() as cursor:
                cursor.execute(query)

    def setUp(self):
        block = Block(name='b1', z=99, ni=1, fe=40, co=0.1,
                      geom=GEOSGeometry('SRID=3125;POINT (591100 1051100)'))
        block.save()
        block = Block(name='b2', z=99, ni=2, fe=42, co=0.2,
                      geom=GEOSGeometry('SRID=3125;POINT (591110 1051100)'))
        block.save()
        block = Block(name='b3', z=102, ni=2, fe=42, co=0.2,
                      geom=GEOSGeometry('SRID=3125;POINT (591100 1051100)'))
        block.save()
        block = Block(name='b4', z=99, ni=1, fe=40, co=0.1,
                      geom=GEOSGeometry('SRID=3125;POINT (591100 1051090)'))
        block.save()
        block = Block(name='b5', z=99, ni=1, fe=40, co=0.1,
                      geom=GEOSGeometry('SRID=3125;POINT (591110 1051090)'))
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

    def test_date_scheduled_lock_if_layout_date(self):
        cluster = Cluster.objects.get(name='c1')
        block = Block.objects.get(name='b1')
        block.cluster = cluster
        block.save()
        cluster.refresh_from_db()
        cluster.date_scheduled = '2020-05-30'
        cluster.save()
        cluster.refresh_from_db()
        cluster.layout_date = '2020-05-31'

        # Okay if same date
        cluster.date_scheduled = '2020-05-30'
        self.assertEqual(None, cluster.save())

        # Fails if updated
        cluster.date_scheduled = '2020-05-19'
        self.assertRaises(ValidationError, cluster.clean)
        self.assertRaises(InternalError, cluster.save)

    def test_excavated_is_set(self):
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

    def test_excavated_is_set_on_update(self):
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

        # Blocks partially excavated
        b4.depth = -1
        b4.save()
        cluster.refresh_from_db()
        self.assertEqual(False, cluster.excavated)

        # Blocks fully excavated
        b5.depth = -1
        b5.save()
        cluster.refresh_from_db()
        self.assertEqual(True, cluster.excavated)

        # Blocks editted
        b5.depth = 1
        b5.save()
        cluster.refresh_from_db()
        self.assertEqual(False, cluster.excavated)

    def test_date_scheduled_lock_if_no_geom(self):
        cluster = Cluster.objects.get(name='c1')
        cluster.date_scheduled = '2020-05-30'
        self.assertRaises(InternalError, cluster.save)

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

    def test_layout_date_lock_if_earlier_than_scheduled(self):
        cluster = Cluster.objects.get(name='c1')
        block = Block.objects.get(name='b1')
        block.cluster = cluster
        block.save()
        cluster.date_scheduled = '2020-05-30'
        cluster.save()
        cluster.layout_date = '2020-05-29'
        self.assertRaises(IntegrityError, cluster.save)

    def test_layout_date_lock_if_no_schedule(self):
        cluster = Cluster.objects.get(name='c1')
        block = Block.objects.get(name='b1')
        block.cluster = cluster
        block.save()
        cluster.layout_date = '2020-05-30'
        self.assertRaises(InternalError, cluster.save)

    def test_layout_date_null_lock_if_excavated(self):
        cluster = Cluster.objects.get(name='c1')
        block = Block.objects.get(name='b1')
        block.cluster = cluster
        block.save()
        cluster.date_scheduled = '2020-05-30'
        cluster.save()
        cluster.layout_date = '2020-05-30'
        cluster.save()
        cluster.excavated = True
        cluster.save()
        cluster.layout_date = None
        self.assertRaises(InternalError, cluster.save)

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

    def test_auto_geom_creation(self):
        drillhole = DrillHole(name='MyOtherHole',
                              x=591070,
                              y=1051100)
        drillhole.save()

        drillhole = DrillHole.objects.get(name='MyOtherHole')
        self.assertEqual(drillhole.geom, GEOSGeometry('SRID=3125;POINT (591070 1051100)'))

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
