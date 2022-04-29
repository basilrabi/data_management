from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils.dateparse import parse_date as pd

from personnel.models.person import Designation, EmploymentRecord, Person


class DesignationTest(TestCase):

    def setUp(self):
        pass

    def test_name_is_unique(self):
        designation = Designation(name='Sampler')
        designation.save()
        designation = Designation(name=' sampler')
        self.assertRaises(IntegrityError, designation.save)


class EmploymentRecordTest(TestCase):

    def setUp(self):
        person = Person(first_name='Basil', last_name='Rabi')
        person.save()

    def test_effectivity_end_is_later_than_start(self):
        person = Person.objects.all().first()

        sampler = Designation(name='Sampler')
        sampler.save()

        employment = EmploymentRecord(
            person=person,
            effectivity=pd('2021-09-04'),
            end=pd('2020-09-04'),
            designation=sampler
        )
        self.assertRaises(ValidationError, employment.clean)

    def test_effectivity_do_not_overlap(self):
        person = Person.objects.all().first()

        sampler = Designation(name='Sampler')
        sampler.save()

        employment = EmploymentRecord(
            person=person,
            effectivity=pd('2019-09-04'),
            end=pd('2020-09-04'),
            designation=sampler
        )
        employment.save()

        employment = EmploymentRecord(
            person=person,
            effectivity=pd('2019-10-04'),
            end=pd('2020-09-04'),
            designation=sampler
        )
        self.assertRaises(ValidationError, employment.clean)

        employment = EmploymentRecord(
            person=person,
            effectivity=pd('2019-08-04'),
            designation=sampler
        )
        self.assertRaises(ValidationError, employment.clean)

        employment = EmploymentRecord(
            person=person,
            effectivity=pd('2019-08-04'),
            end=pd('2019-08-31'),
            designation=sampler
        )
        self.assertEqual(None, employment.clean())

        employment = EmploymentRecord(
            person=person,
            effectivity=pd('2020-09-05'),
            end=pd('2021-09-04'),
            designation=sampler
        )
        self.assertEqual(None, employment.clean())
