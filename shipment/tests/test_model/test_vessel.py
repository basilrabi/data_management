from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from shipment.models.dso import Vessel

class  VesselTest(TestCase):

    def setUp(self):
        pass

    def test_name_is_capitalized(self):
        # pylint: disable=E1101
        vesselA = Vessel(name='PM Hayabusa')
        vesselA.save()
        test_name = Vessel.objects.all().first().name
        self.assertEqual(test_name, 'PM HAYABUSA')

    def test_name_is_not_duplicated(self):
        vessel = Vessel(name='PM Hayabusa')
        vessel.save()

        vessel = Vessel(name='PM HAYABUSA')
        self.assertRaises(IntegrityError, vessel.save)

    def test_name_is_not_duplicated_with_lead_and_trail_space(self):
        vessel = Vessel(name='PM Hayabusa')
        vessel.save()

        vessel = Vessel(name=' PM HAYABUSA ')
        self.assertRaises(IntegrityError, vessel.save)

    def test_name_is_not_duplicated_with_excess_space(self):
        vessel = Vessel(name='PM Hayabusa')
        vessel.save()

        vessel = Vessel(name=' PM  HAYABUSA')
        self.assertRaises(IntegrityError, vessel.save)
