from django.db.utils import IntegrityError
from django.test import TestCase

from location.models.source import MineBlock, Stockyard

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
        yard = Stockyard(ridge='T1', name='LDA 1')
        yard.save()
        yard = Stockyard(ridge='T2', name='LDA 1')
        self.assertEqual(None, yard.save())
        yard = Stockyard(ridge='T1', name='LDA-1')
        self.assertRaises(IntegrityError, yard.save)
