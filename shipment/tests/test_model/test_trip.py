from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.dateparse import parse_datetime as pd

from custom.functions import setup_triggers
from shipment.models.dso import (
    LayDaysDetail, LayDaysStatement, Shipment, Vessel
)
from shipment.models.lct import LCT, Trip, TripDetail

# pylint: disable=no-member

class  TripTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        setup_triggers()

    def setUp(self):
        lct = LCT(name='guagua', capacity=1000)
        lct.save()
        vessel = Vessel(name='PM Hayabusa')
        vessel.save()

    def test_continuity(self):
        lct = LCT.objects.all().first()
        vessel = Vessel.objects.all().first()

        # Only one trip is continuous
        trip = Trip(lct=lct,
                    vessel=vessel,
                    status='loaded',
                    dump_truck_trips=50,
                    vessel_grab=2)
        trip.save()
        trip_detail = TripDetail(
            trip=trip,
            interval_from=pd('2019-08-16 00:00:00+0800'),
            interval_class='preparation_loading'
        )
        trip_detail.save()
        trip_detail = TripDetail(
            trip=trip,
            interval_from=pd('2019-08-16 00:05:00+0800'),
            interval_class='loading'
        )
        trip_detail.save()

        trip = Trip.objects.get(dump_truck_trips=50)
        self.assertEqual(trip._continuous(), True)

        # Another adjacent trip is continous
        trip = Trip(lct=lct,
                    vessel=vessel,
                    status='loaded',
                    dump_truck_trips=51,
                    vessel_grab=2)
        trip.save()
        trip_detail = TripDetail(
            trip=trip,
            interval_from=pd('2019-08-16 00:05:00+0800'),
            interval_class='preparation_loading'
        )
        trip_detail.save()
        trip_detail = TripDetail(
            trip=trip,
            interval_from=pd('2019-08-16 00:10:00+0800'),
            interval_class='loading'
        )
        trip_detail.save()

        trip = Trip.objects.get(dump_truck_trips=50)
        self.assertEqual(trip._continuous(), True)
        trip = Trip.objects.get(dump_truck_trips=51)
        self.assertEqual(trip._continuous(), True)

        # Another adjacent trip but broken
        trip = Trip(lct=lct,
                    vessel=vessel,
                    status='loaded',
                    dump_truck_trips=52,
                    vessel_grab=2)
        trip.save()
        trip_detail = TripDetail(
            trip=trip,
            interval_from=pd('2019-08-16 00:15:00+0800'),
            interval_class='preparation_loading'
        )
        trip_detail.save()
        trip_detail = TripDetail(
            trip=trip,
            interval_from=pd('2019-08-16 00:20:00+0800'),
            interval_class='loading'
        )
        trip_detail.save()

        trip = Trip.objects.get(dump_truck_trips=50)
        self.assertEqual(trip._continuous(), True)
        trip = Trip.objects.get(dump_truck_trips=51)
        self.assertEqual(trip._continuous(), False)
        trip = Trip.objects.get(dump_truck_trips=52)
        self.assertEqual(trip._continuous(), False)

    def test_data_is_complete_if_not_rejected(self):
        lct = LCT.objects.all().first()
        vessel = Vessel.objects.all().first()
        trip = Trip(lct=lct,
                    vessel=vessel,
                    status='loaded',
                    dump_truck_trips=50,
                    vessel_grab=2)
        self.assertEqual(trip.clean(), None)
        self.assertEqual(trip.dump_truck_trips, 50)
        self.assertEqual(trip.vessel_grab, 2)

        trip = Trip(lct=lct, vessel=vessel, status='partial', vessel_grab=2)
        self.assertRaises(ValidationError, trip.clean)

        trip = Trip(lct=lct,
                    vessel=vessel,
                    status='partial',
                    dump_truck_trips=20)
        self.assertRaises(ValidationError, trip.clean)

    def test_data_is_okay_if_rejected(self):
        lct = LCT.objects.all().first()
        vessel = Vessel.objects.all().first()
        trip = Trip(lct=lct, vessel=vessel, status='rejected')
        self.assertEqual(trip.clean(), None)
        self.assertEqual(trip.dump_truck_trips, 0)
        self.assertEqual(trip.vessel_grab, 0)

    def test_if_trigger_works(self):
        lct = LCT.objects.all().first()
        vessel = Vessel.objects.all().first()

        # No trip details
        trip = Trip(lct=lct,
                    vessel=vessel,
                    status='loaded',
                    dump_truck_trips=50,
                    vessel_grab=2)
        trip.save()
        trip = Trip.objects.all().first()
        self.assertEqual(trip.interval_from, None)
        self.assertEqual(trip.interval_to, None)
        self.assertEqual(trip.valid, False)

        # One detail
        trip_detail = TripDetail(
            trip=trip,
            interval_from=pd('2019-08-16 00:00:00+0800'),
            interval_class='preparation_loading'
        )
        trip_detail.save()
        trip = Trip.objects.all().first()
        self.assertEqual(trip.interval_from, pd('2019-08-16 00:00:00+0800'))
        self.assertEqual(trip.interval_to, None)
        self.assertEqual(trip.valid, False)

        # Two details
        trip_detail = TripDetail(
            trip=trip,
            interval_from=pd('2019-08-16 00:05:00+0800'),
            interval_class='loading'
        )
        trip_detail.save()
        trip = Trip.objects.all().first()
        self.assertEqual(trip.interval_from, pd('2019-08-16 00:00:00+0800'))
        self.assertEqual(trip.interval_to, pd('2019-08-16 00:05:00+0800'))
        self.assertEqual(trip.valid, False)

        # Valid shipment
        shipment = Shipment(name='284', vessel=vessel)
        shipment.save()
        statement = LayDaysStatement(
            shipment=shipment,
            commenced_loading=pd('2019-08-16 10:00:00+0800'),
            completed_loading=pd('2019-08-16 20:00:00+0800')
        )
        statement.save()
        trip_detail = TripDetail(
            trip=trip,
            interval_from=pd('2019-08-16 10:05:00+0800'),
            interval_class='preparation_departure'
        )
        trip_detail.save()
        trip = Trip.objects.all().first()
        self.assertEqual(trip.interval_from, pd('2019-08-16 00:00:00+0800'))
        self.assertEqual(trip.interval_to, pd('2019-08-16 10:05:00+0800'))
        self.assertEqual(trip.valid, True)

        # Become invalid again
        trip_detail = trip.tripdetail_set.all().last()
        trip_detail.delete()
        trip = Trip.objects.all().first()
        self.assertEqual(trip.interval_from, pd('2019-08-16 00:00:00+0800'))
        self.assertEqual(trip.interval_to, pd('2019-08-16 00:05:00+0800'))
        self.assertEqual(trip.valid, False)

    def test_trip_validity_recheck_upon_shipment_detail_update(self):
        lct = LCT.objects.all().first()
        vessel = Vessel.objects.all().first()
        shipment = Shipment(name='284', vessel=vessel)
        shipment.save()
        statement = LayDaysStatement(
            shipment=shipment,
            commenced_loading=pd('2019-08-16 10:00:00+0800'),
            completed_loading=pd('2019-08-16 20:00:00+0800')
        )
        statement.save()

        trip = Trip(lct=lct,
                    vessel=vessel,
                    status='loaded',
                    dump_truck_trips=50,
                    vessel_grab=2)
        trip.save()
        trip_detail = TripDetail(
            trip=trip,
            interval_from=pd('2019-08-16 00:00:00+0800'),
            interval_class='preparation_loading'
        )
        trip_detail.save()
        trip_detail = TripDetail(
            trip=trip,
            interval_from=pd('2019-08-16 10:05:00+0800'),
            interval_class='preparation_departure'
        )
        trip_detail.save()

        self.assertEqual(trip.valid, True)
        statement.commenced_loading=pd('2019-08-16 10:06:00+0800')
        statement.save()
        trip = Trip.objects.all().first()
        self.assertEqual(trip.valid, False)
