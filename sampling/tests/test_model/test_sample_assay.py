from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.dateparse import parse_date as pd

from fleet.models.equipment import TrackedExcavator
from location.models.source import MineBlock, Stockyard
from personnel.models.person import Designation, EmploymentRecord, Person
from sampling.models.piling import PilingMethod, TripsPerPile
from sampling.models.proxy import MiningSampleAssay
from sampling.models.sample import (Material,
                                    MiningSample,
                                    MiningSampleIncrement,
                                    MiningSampleReport)

# pylint: disable=no-member

class MiningSampleAssayTest(TestCase):

    def setUp(self):
        method = PilingMethod(name='PRE PILE')
        method.save()
        trips = TripsPerPile(piling_method=method,
                             effectivity=pd('2019-01-01'),
                             trips=10)
        trips.save()
        d1 = Designation(name='Mine Foreman')
        d2 = Designation(name='Mine Supervisor')
        d3 = Designation(name='Sampler')
        d1.save()
        d2.save()
        d3.save()
        p1 = Person(first_name='A', last_name='A')
        p2 = Person(first_name='B', last_name='B')
        p3 = Person(first_name='C', last_name='C')
        p1.save()
        p2.save()
        p3.save()
        e1 = EmploymentRecord(person=p1,
                              effectivity=pd('2019-01-01'),
                              designation=d1)
        e2 = EmploymentRecord(person=p2,
                              effectivity=pd('2019-01-01'),
                              designation=d2)
        e3 = EmploymentRecord(person=p3,
                              effectivity=pd('2019-01-01'),
                              designation=d3)
        e1.save()
        e2.save()
        e3.save()
        mat1 = Material(name='LF')
        mat1.save()
        mb1 = MineBlock(name='101', ridge='T3')
        mb1.save()
        my1 = Stockyard(name='MY201')
        my1.save()
        tx = TrackedExcavator(fleet_number=1)
        tx.save()
        s1 = MiningSample(series_number=1,
                          material=mat1,
                          dumping_area=my1,
                          piling_method=method)
        s1.save()
        r1 = MiningSampleReport(date=pd('2019-09-05'),
                                shift_collected='N',
                                piling_method=method,
                                material=mat1,
                                tx=tx,
                                dumping_area=my1,
                                supervisor=p2,
                                foreman=p1)
        r1.save()
        r1.sampler.add(p3)
        r1.save()
        i1 = MiningSampleIncrement(sample=s1, report=r1, trips=10)
        i1.save()

    def test_assay_dates(self):
        assay = MiningSampleAssay.objects.all().first()
        self.assertEqual(None, assay.date_received_for_preparation)
        self.assertEqual(None, assay.date_prepared)
        self.assertEqual(None, assay.date_received_for_analysis)
        self.assertEqual(None, assay.date_analyzed)
        self.assertEqual(None, assay.ni)
        self.assertEqual(None, assay.fe)
        self.assertEqual(None, assay.co)
        self.assertEqual(None, assay.moisture)
        assay.ni = 1.05
        self.assertRaises(ValidationError, assay.clean)
        assay.date_analyzed = pd('2019-09-06')
        self.assertRaises(ValidationError, assay.clean)
        assay.date_received_for_analysis = pd('2019-09-07')
        self.assertRaises(ValidationError, assay.clean)
        assay.date_prepared = pd('2019-09-08')
        self.assertRaises(ValidationError, assay.clean)
        assay.date_received_for_preparation = pd('2019-09-09')
        self.assertRaises(ValidationError, assay.clean)
        assay.date_received_for_analysis = pd('2019-09-06')
        assay.date_prepared = pd('2019-09-06')
        assay.date_received_for_preparation = pd('2019-09-06')
        self.assertEqual(None, assay.clean())
        assay.date_received_for_analysis = pd('2019-09-05')
        assay.date_prepared = pd('2019-09-04')
        assay.date_received_for_preparation = pd('2019-09-03')
        self.assertEqual(None, assay.clean())
