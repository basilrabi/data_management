from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils.dateparse import parse_date as pd

from fleet.models.equipment import TrackedExcavator
from location.models.source import MineBlock, Stockyard
from personnel.models.person import Designation, EmploymentRecord, Person
from sampling.models.piling import PilingMethod, TripsPerPile
from sampling.models.sample import (MiningSample,
                                    MiningSampleIncrement,
                                    MiningSampleReport)

# pylint: disable=no-member

class MiningSampleReportTest(TestCase):

    def setUp(self):
        method = PilingMethod(name='PRE PILE')
        method.save()
        trips = TripsPerPile(piling_method=method,
                             effectivity=pd('2019-01-01'),
                             trips=10)
        trips.save()
        method = PilingMethod(name='DIRECT DUMP')
        method.save()
        trips = TripsPerPile(piling_method=method,
                             effectivity=pd('2019-07-01'),
                             trips=20)
        trips.save()

        d1 = Designation(name='Mine Foreman')
        d2 = Designation(name='Mine Supervisor')
        d3 = Designation(name='Data Analyst')
        d4 = Designation(name='Kapwa')
        d5 = Designation(name='Sampler')
        d1.save()
        d2.save()
        d3.save()
        d4.save()
        d5.save()

        p1 = Person(first_name='A', last_name='A')
        p2 = Person(first_name='B', last_name='B')
        p3 = Person(first_name='C', last_name='C')
        p4 = Person(first_name='D', last_name='D')
        p5 = Person(first_name='E', last_name='E')
        p1.save()
        p2.save()
        p3.save()
        p4.save()
        p5.save()

        e1 = EmploymentRecord(person=p1,
                              effectivity=pd('2019-01-01'),
                              designation=d1)
        e2 = EmploymentRecord(person=p2,
                              effectivity=pd('2019-01-01'),
                              designation=d2)
        e3 = EmploymentRecord(person=p3,
                              effectivity=pd('2019-01-01'),
                              designation=d3)
        e4 = EmploymentRecord(person=p4,
                              effectivity=pd('2019-01-01'),
                              designation=d4)
        e5 = EmploymentRecord(person=p5,
                              effectivity=pd('2019-01-01'),
                              designation=d5)
        e1.save()
        e2.save()
        e3.save()
        e4.save()
        e5.save()

        mb1 = MineBlock(name='101', ridge='T3')
        mb2 = MineBlock(name='201', ridge='T1')
        mb1.save()
        mb2.save()
        my1 = Stockyard(name='MY201')
        my2 = Stockyard(name='MY301')
        my1.save()
        my2.save()
        tx = TrackedExcavator(fleet_number=1)
        tx.save()

    def test_right_personnel_and_method_are_assigned(self):
        p1 = Person.objects.get(first_name='A')
        p2 = Person.objects.get(first_name='B')
        p3 = Person.objects.get(first_name='C')
        p4 = Person.objects.get(first_name='D')
        p5 = Person.objects.get(first_name='E')
        m1 = PilingMethod.objects.get(name='PRE PILE')
        m2 = PilingMethod.objects.get(name='DIRECT DUMP')
        my1 = Stockyard.objects.get(name='MY201')
        tx = TrackedExcavator.objects.get(fleet_number=1)

        r1 = MiningSampleReport(date=pd('2019-09-05'),
                                shift_collected='D',
                                piling_method=m1,
                                dumping_area=my1,
                                supervisor=p2,
                                foreman=p1)
        r1.save()
        r1.tx.add(tx)
        r1.sampler.add(p5)
        self.assertEqual(None, r1.clean())

        r2 = MiningSampleReport(date=pd('2019-09-05'),
                                shift_collected='N',
                                piling_method=m1,
                                dumping_area=my1,
                                supervisor=p2,
                                foreman=p4)
        r2.save()
        r2.tx.add(tx)
        r2.sampler.add(p5)
        self.assertRaises(ValidationError, r2.clean)

        r3 = MiningSampleReport(date=pd('2019-09-05'),
                                shift_collected='D',
                                piling_method=m1,
                                dumping_area=my1,
                                supervisor=p3,
                                foreman=p1)
        r3.save()
        r3.tx.add(tx)
        r3.sampler.add(p5)
        self.assertRaises(ValidationError, r3.clean)

        r4 = MiningSampleReport(date=pd('2019-09-05'),
                                shift_collected='D',
                                piling_method=m1,
                                dumping_area=my1,
                                supervisor=p2,
                                foreman=p1)
        r4.save()
        r4.tx.add(tx)
        r4.sampler.add(p3)
        self.assertRaises(ValidationError, r4.clean)

        r5 = MiningSampleReport(date=pd('2019-05-05'),
                                shift_collected='D',
                                piling_method=m2,
                                dumping_area=my1,
                                supervisor=p2,
                                foreman=p1)
        r5.save()
        r5.tx.add(tx)
        r5.sampler.add(p5)
        self.assertRaises(ValidationError, r4.clean)

    def mining_sample_increments_matches_the_samples(self):
        m1 = PilingMethod.objects.get(name='PRE PILE')
        m2 = PilingMethod.objects.get(name='DIRECT DUMP')
        my1 = Stockyard.objects.get(name='MY201')
        my2 = Stockyard.objects.get(name='MY301')
        p1 = Person.objects.get(first_name='A')
        p2 = Person.objects.get(first_name='B')
        p5 = Person.objects.get(first_name='E')
        tx = TrackedExcavator.objects.get(fleet_number=1)

        s1 = MiningSample(series_number=1,
                          dumping_area=my1,
                          piling_method=m1)
        s1.save()

        r1 = MiningSampleReport(date=pd('2019-09-05'),
                                shift_collected='N',
                                piling_method=m1,
                                dumping_area=my1,
                                supervisor=p2,
                                foreman=p1)
        r1.save()
        r1.tx.add(tx)
        r1.sampler.add(p5)
        r1.save()

        i1 = MiningSampleIncrement(sample=s1, report=r1, trips=10)
        i1.save()

        r2 = MiningSampleReport(date=pd('2019-09-06'),
                                shift_collected='D',
                                piling_method=m2,
                                dumping_area=my1,
                                supervisor=p2,
                                foreman=p1)
        r2.save()
        r2.tx.add(tx)
        r2.sampler.add(p5)
        r2.save()

        i2 = MiningSampleIncrement(sample=s1, report=r2, trips=10)
        self.assertRaises(ValidationError, i2.clean)

        r2 = MiningSampleReport(date=pd('2019-09-06'),
                                shift_collected='D',
                                piling_method=m1,
                                dumping_area=my1,
                                supervisor=p2,
                                foreman=p1)
        r2.save()
        r2.tx.add(tx)
        r2.sampler.add(p5)
        r2.save()

        i2 = MiningSampleIncrement(sample=s1, report=r2, trips=10)
        self.assertRaises(ValidationError, i2.clean)

        r2 = MiningSampleReport(date=pd('2019-09-06'),
                                shift_collected='D',
                                piling_method=m1,
                                dumping_area=my1,
                                supervisor=p2,
                                foreman=p1)
        r2.save()
        r2.tx.add(tx)
        r2.sampler.add(p5)
        r2.save()

        i2 = MiningSampleIncrement(sample=s1, report=r2, trips=10)
        self.assertRaises(ValidationError, i2.clean)

        r2 = MiningSampleReport(date=pd('2019-09-06'),
                                shift_collected='D',
                                piling_method=m1,
                                dumping_area=my2,
                                supervisor=p2,
                                foreman=p1)
        r2.save()
        r2.tx.add(tx)
        r2.sampler.add(p5)
        r2.save()

        i2 = MiningSampleIncrement(sample=s1, report=r2, trips=10)
        self.assertRaises(ValidationError, i2.clean)

    def test_sample_reports_are_being_added_correctly(self):
        m1 = PilingMethod.objects.get(name='PRE PILE')
        my1 = Stockyard.objects.get(name='MY201')
        p1 = Person.objects.get(first_name='A')
        p2 = Person.objects.get(first_name='B')
        p5 = Person.objects.get(first_name='E')
        tx = TrackedExcavator.objects.get(fleet_number=1)

        s1 = MiningSample(series_number=1,
                          dumping_area=my1,
                          piling_method=m1)
        s1.save()

        r1 = MiningSampleReport(date=pd('2019-09-05'),
                                shift_collected='N',
                                piling_method=m1,
                                dumping_area=my1,
                                supervisor=p2,
                                foreman=p1)
        r1.save()
        r1.tx.add(tx)
        r1.sampler.add(p5)
        r1.save()
        i1 = MiningSampleIncrement(sample=s1, report=r1, trips=5)
        i1.save()

        self.assertEqual(True, s1.has_increment())
        self.assertEqual(10, s1.required_trips())
        self.assertEqual(5, s1.trips)
        self.assertEqual(pd('2019-09-05'), s1.start_collection)
        self.assertEqual(2019, s1.year)
        self.assertEqual(False, s1.ready_for_delivery)

        r1 = MiningSampleReport(date=pd('2019-09-06'),
                                shift_collected='D',
                                piling_method=m1,
                                dumping_area=my1,
                                supervisor=p2,
                                foreman=p1)
        r1.save()
        r1.tx.add(tx)
        r1.sampler.add(p5)
        r1.save()
        i1 = MiningSampleIncrement(sample=s1, report=r1, trips=5)
        self.assertEqual(False, hasattr(s1, 'assay'))
        i1.save()
        self.assertEqual(10, s1.trips)

        r1 = MiningSampleReport(date=pd('2019-09-06'),
                                shift_collected='N',
                                piling_method=m1,
                                dumping_area=my1,
                                supervisor=p2,
                                foreman=p1)
        r1.save()
        r1.tx.add(tx)
        r1.sampler.add(p5)
        r1.save()
        i1 = MiningSampleIncrement(sample=s1, report=r1, trips=5)
        self.assertRaises(ValidationError, i1.clean)
        self.assertEqual(True, s1.ready_for_delivery)

    def test_sample_is_not_duplicated_in_report(self):
        m1 = PilingMethod.objects.get(name='PRE PILE')
        my1 = Stockyard.objects.get(name='MY201')
        p1 = Person.objects.get(first_name='A')
        p2 = Person.objects.get(first_name='B')
        p5 = Person.objects.get(first_name='E')
        tx = TrackedExcavator.objects.get(fleet_number=1)

        s1 = MiningSample(series_number=1,
                          dumping_area=my1,
                          piling_method=m1)
        s1.save()

        r1 = MiningSampleReport(date=pd('2019-09-05'),
                                shift_collected='N',
                                piling_method=m1,
                                dumping_area=my1,
                                supervisor=p2,
                                foreman=p1)
        r1.save()
        r1.tx.add(tx)
        r1.sampler.add(p5)
        r1.save()
        i1 = MiningSampleIncrement(sample=s1, report=r1, trips=5)
        i1.save()
        i1 = MiningSampleIncrement(sample=s1, report=r1, trips=5)
        self.assertRaises(IntegrityError, i1.save)

    def test_sample_is_not_ready_without_increments(self):
        m1 = PilingMethod.objects.get(name='PRE PILE')
        my1 = Stockyard.objects.get(name='MY201')
        s1 = MiningSample(series_number=1,
                          dumping_area=my1,
                          piling_method=m1,
                          ready_for_delivery=True)
        self.assertRaises(ValidationError, s1.clean)
