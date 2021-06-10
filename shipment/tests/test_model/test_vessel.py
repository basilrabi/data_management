from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from shipment.models.dso import Vessel

# pylint: disable=no-member


class  VesselTest(TestCase):

    def setUp(self):
        pass

    def test_name_is_capitalized(self):
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

    def test_if_not_duplicated_with_mv_a(self):
        vessel = Vessel(name='MV PM Hayabusa')
        vessel.save()

        vessel = Vessel(name='MV PM  HAYABUSA')
        self.assertRaises(IntegrityError, vessel.save)

    def test_if_not_duplicated_with_mv_b(self):
        vessel = Vessel(name='MV PM Hayabusa')
        vessel.save()

        vessel = Vessel(name=' M/V PM-HAYABUSA')
        self.assertRaises(IntegrityError, vessel.save)

    def test_if_not_duplicated_with_mv_c(self):
        vessel = Vessel(name='PM Hayabusa')
        vessel.save()

        vessel = Vessel(name=' M/V PM-HAYABUSA')
        self.assertRaises(IntegrityError, vessel.save)

    def test_if_not_duplicated_with_mv_d(self):
        vessel = Vessel(name='PM Hayabusa')
        vessel.save()

        vessel = Vessel(name=' M/V PM-HAYABUSA')
        self.assertRaises(ValidationError, vessel.clean)
