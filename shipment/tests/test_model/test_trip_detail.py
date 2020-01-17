from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.dateparse import parse_datetime as pd

from shipment.models.dso import Shipment, Vessel
from shipment.models.lct import LCT, LCTContract, Trip, TripDetail

# pylint: disable=no-member

class  TripDetailTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        lct = LCT(name='guagua', capacity=1000)
        lct.save()
        lct_contract = LCTContract(
            lct=lct, start='2019-08-01', end='2019-08-30'
        )
        lct_contract.save()
        vessel = Vessel(name='guagua')
        vessel.save()
        shipment = Shipment(
            name='284', vessel=vessel,
            start_loading=pd('2019-08-17 00:00:00+0800'),
            end_loading=pd('2019-08-19 00:00:00+0800')
        )
        shipment.save()

    def setUp(self):
        lct = LCT.objects.all().first()
        vessel = Vessel.objects.all().first()
        trip = Trip(lct=lct,
                    vessel=vessel,
                    status='loaded',
                    dump_truck_trips=50,
                    vessel_grab=2)
        trip.save()

    def test_trip_with_valid_inputs(self):
        trip = Trip.objects.all().first()

        trip_detail1 = TripDetail(
            trip=trip,
            interval_from=pd('2019-08-16 00:00:00+0800'),
            interval_class='preparation_loading'
        )
        self.assertEqual(trip_detail1.clean(), None)
        trip_detail1.save()

        trip_detail2 = TripDetail(
            trip=trip,
            interval_from=pd('2019-08-16 00:05:00+0800'),
            interval_class='preparation_loading'
        )
        self.assertEqual(trip_detail2.clean(), None)
        trip_detail2.save()

        trip = Trip.objects.all().first()

        self.assertEqual(trip._interval_from(),
                         trip_detail1.interval_from)
        self.assertEqual(trip._interval_to(),
                         trip_detail2.interval_from)

    def test_trip_with_the_same_time(self):
        trip = Trip.objects.all().first()
        trip_detail = TripDetail(
            trip=trip,
            interval_from=pd('2019-08-16 00:00:00+0800'),
            interval_class='preparation_loading'
        )
        trip_detail.save()
        trip_detail = TripDetail(
            trip=trip,
            interval_from=pd('2019-08-16 00:00:00+0800'),
            interval_class='preparation_loading'
        )
        self.assertRaises(ValidationError, trip_detail.clean)

    def test_overlapping_lct_trips(self):
        trip = Trip.objects.all().first()
        lct = LCT.objects.all().first()
        vessel = Vessel.objects.all().first()

        trip_detail = TripDetail(
            trip=trip,
            interval_from=pd('2019-08-16 00:00:00+0800'),
            interval_class='preparation_loading'
        )
        trip_detail.save()

        trip_detail = TripDetail(
            trip=trip,
            interval_from=pd('2019-08-16 00:05:00+0800'),
            interval_class='preparation_loading'
        )
        trip_detail.save()

        trip2 = Trip(lct=lct,
                    vessel=vessel,
                    status='loaded',
                    dump_truck_trips=50,
                    vessel_grab=2)
        trip2.save()

        trip_detail = TripDetail(
            trip=trip2,
            interval_from=pd('2019-08-16 00:04:00+0800'),
            interval_class='preparation_loading'
        )
        self.assertRaises(ValidationError, trip_detail.clean)

        trip_detail = TripDetail(
            trip=trip2,
            interval_from=pd('2019-08-15 12:00:00+0800'),
            interval_class='preparation_loading'
        )
        trip_detail.save()
        trip_detail = TripDetail(
            trip=trip2,
            interval_from=pd('2019-08-20 12:00:00+0800'),
            interval_class='preparation_loading'
        )
        self.assertRaises(ValidationError, trip_detail.clean)

    def test_lct_not_yet_rented(self):
        trip = Trip.objects.all().first()

        trip_detail = TripDetail(
            trip=trip,
            interval_from=pd('2019-07-16 00:04:00+0800'),
            interval_class='preparation_loading'
        )
        self.assertRaises(ValidationError, trip_detail.clean)

        trip_detail = TripDetail(
            trip=trip,
            interval_from=pd('2019-09-16 00:04:00+0800'),
            interval_class='preparation_loading'
        )
        self.assertRaises(ValidationError, trip_detail.clean)

    def test_only_one_end_per_detail(self):
        trip = Trip.objects.all().first()
        trip_detail = TripDetail(
            trip=trip,
            interval_from=pd('2019-08-16 00:00:00+0800'),
            interval_class='preparation_loading'
        )
        trip_detail.save()
        trip_detail = TripDetail(
            trip=trip,
            interval_from=pd('2019-08-17 00:00:00+0800'),
            interval_class='end'
        )
        trip_detail.save()
        trip_detail = TripDetail(
            trip=trip,
            interval_from=pd('2019-08-17 00:00:00+0800'),
            interval_class='end'
        )
        self.assertRaises(ValidationError, trip_detail.clean)
