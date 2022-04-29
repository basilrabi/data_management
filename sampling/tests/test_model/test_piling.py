from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils.dateparse import parse_date as pd

from sampling.models.piling import PilingMethod, TripsPerPile


class PilingMethodTest(TestCase):

    def setUp(self):
        pass

    def test_name_is_capitalized(self):
        method = PilingMethod(name='pre-pile')
        method.save()
        test_name = PilingMethod.objects.all().first().name
        self.assertEqual(test_name, 'PRE-PILE')

    def test_name_is_not_duplicated(self):
        method = PilingMethod(name='direct dump')
        method.save()
        method = PilingMethod(name='direct Dump')
        self.assertRaises(IntegrityError, method.save)


class TripsPerPileTest(TestCase):

    def setUp(self):
        method = PilingMethod(name='pre-pile')
        method.save()

    def test_trips_validity(self):
        method = PilingMethod.objects.all().first()
        trips_per_pile = TripsPerPile(piling_method=method,
                                      effectivity=pd('2019-01-01'),
                                      end=pd('2019-02-01'),
                                      trips=10)
        self.assertEqual(trips_per_pile.clean(), None)

        trips_per_pile = TripsPerPile(piling_method=method,
                                      effectivity=pd('2019-02-01'),
                                      end=pd('2019-01-01'),
                                      trips=10)
        self.assertRaises(ValidationError, trips_per_pile.clean)

    def test_effectivity_do_not_overlap(self):
        method = PilingMethod.objects.all().first()
        trips_per_pile = TripsPerPile(piling_method=method,
                                      effectivity=pd('2019-01-01'),
                                      end=pd('2019-02-01'),
                                      trips=10)
        trips_per_pile.save()

        trips_per_pile = TripsPerPile(piling_method=method,
                                      effectivity=pd('2019-02-01'),
                                      trips=10)
        self.assertRaises(ValidationError, trips_per_pile.clean)

        trips_per_pile = TripsPerPile(piling_method=method,
                                      effectivity=pd('2019-02-02'),
                                      trips=10)
        self.assertEqual(None, trips_per_pile.clean())

        trips_per_pile = TripsPerPile(piling_method=method,
                                      effectivity=pd('2018-02-01'),
                                      trips=10)
        self.assertRaises(ValidationError, trips_per_pile.clean)

        trips_per_pile = TripsPerPile(piling_method=method,
                                      effectivity=pd('2018-02-01'),
                                      end=pd('2018-12-31'),
                                      trips=10)
        self.assertEqual(None, trips_per_pile.clean())

    def test_effectivity_do_not_have_gaps(self):
        method = PilingMethod.objects.all().first()
        trips_per_pile = TripsPerPile(piling_method=method,
                                      effectivity=pd('2019-01-01'),
                                      end=pd('2019-02-01'),
                                      trips=10)
        trips_per_pile.save()

        trips_per_pile = TripsPerPile(piling_method=method,
                                      effectivity=pd('2018-02-01'),
                                      end=pd('2018-12-30'),
                                      trips=10)
        self.assertRaises(ValidationError, trips_per_pile.clean)

        trips_per_pile = TripsPerPile(piling_method=method,
                                      effectivity=pd('2019-02-03'),
                                      trips=10)
        self.assertRaises(ValidationError, trips_per_pile.clean)
