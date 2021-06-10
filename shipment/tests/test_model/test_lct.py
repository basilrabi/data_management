from django.db.utils import IntegrityError
from django.test import TestCase

from shipment.models.lct import LCT

# pylint: disable=no-member


class  LCTTest(TestCase):

    def setUp(self):
        pass

    def test_name_is_capitalized(self):
        lctA = LCT(name='guagua', capacity=1000)
        lctA.save()
        test_name = LCT.objects.all().first().name
        self.assertEqual(test_name, 'GUAGUA')

    def test_name_is_not_duplicated(self):
        lct = LCT(name='guagua', capacity=1000)
        lct.save()
        lct = LCT(name='Guagua', capacity=1000)
        self.assertRaises(IntegrityError, lct.save)
