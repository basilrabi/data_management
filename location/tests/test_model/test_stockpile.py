from django.db.utils import IntegrityError
from django.test import TestCase

from location.models.source import Stockpile


class StockpileTest(TestCase):

    def setUp(self):
        pass

    def test_name_is_unique_per_ridge_part(self):
        yard = Stockpile(name='LDA 1')
        yard.save()
        yard = Stockpile(name='LDA  1')
        self.assertRaises(IntegrityError, yard.save)
