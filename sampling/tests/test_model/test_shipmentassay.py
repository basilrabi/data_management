from django.test import TestCase

from sampling.models.proxy import PamcoShipmentAssay
from sampling.models.sample import (
    Laboratory,
    ShipmentDischargeLotAssay,
    ShipmentLoadingAssay,
    ShipmentLoadingLotAssay
)
from shipment.models.dso import Destination, Shipment, Vessel

# pylint: disable=no-member


class PamcoShipmentAssayTest(TestCase):

    def setUp(self):
        vessel = Vessel(name='New Beginning')
        vessel.save()
        shipment = Shipment(name='282', vessel=vessel)
        shipment.save()

    def test_correct_computation(self):
        laboratory = Laboratory(name='PAMCO')
        laboratory.save()
        shipment = Shipment.objects.first()
        assay = PamcoShipmentAssay(
            laboratory=laboratory, shipment=shipment, co=0.07, cr=0.92, mn=0.30,
            fe=16.49, sio2=33.7, cao=0.02, mgo=25.38, al2o3=0.93, p=0.0004,
            s=0.015, ignition_loss=12.26

        )
        assay.save()
        lot = ShipmentDischargeLotAssay(shipment_assay=assay, lot=1, wmt=4901.5, moisture=32.92, ni=1.73)
        lot.save()
        lot = ShipmentDischargeLotAssay(shipment_assay=assay, lot=2, wmt=4901.5, moisture=32.99, ni=1.71)
        lot.save()
        lot = ShipmentDischargeLotAssay(shipment_assay=assay, lot=3, wmt=4901.5, moisture=33.21, ni=1.71)
        lot.save()
        lot = ShipmentDischargeLotAssay(shipment_assay=assay, lot=4, wmt=4901.5, moisture=33.12, ni=1.73)
        lot.save()
        lot = ShipmentDischargeLotAssay(shipment_assay=assay, lot=5, wmt=4901.5, moisture=32.96, ni=1.73)
        lot.save()
        lot = ShipmentDischargeLotAssay(shipment_assay=assay, lot=6, wmt=4901.5, moisture=32.90, ni=1.74)
        lot.save()
        lot = ShipmentDischargeLotAssay(shipment_assay=assay, lot=7, wmt=4901.5, moisture=31.46, ni=1.76)
        lot.save()
        lot = ShipmentDischargeLotAssay(shipment_assay=assay, lot=8, wmt=4901.5, moisture=32.10, ni=1.75)
        lot.save()
        lot = ShipmentDischargeLotAssay(shipment_assay=assay, lot=9, wmt=4901.5, moisture=32.73, ni=1.76)
        lot.save()
        lot = ShipmentDischargeLotAssay(shipment_assay=assay, lot=10, wmt=4901.5, moisture=32.60, ni=1.75)
        lot.save()
        assay.refresh_from_db()

        self.assertEqual(float(assay.bc()), 0.75)
        self.assertEqual(float(assay.dmt), 32987.586)
        self.assertEqual(float(assay.moisture), 32.7)
        self.assertEqual(float(assay.ni), 1.74)
        self.assertEqual(assay.wmt, 49015)


class ShipmentLoadingAssayTest(TestCase):

    def setUp(self):
        vessel = Vessel(name='Jin Hong')
        vessel.save()
        shipment = Shipment(name='481-C', vessel=vessel)
        shipment.save()

    def test_correct_computation(self):
        shipment = Shipment.objects.first()
        assay = ShipmentLoadingAssay(
            date='2020-07-29', shipment=shipment,
            fe=16.02, mgo=26.49, sio2=34.24, cr=0.86
        )
        assay.save()
        lot = ShipmentLoadingLotAssay(shipment_assay=assay, lot=1, wmt=5087.897, moisture=30.75, ni=1.44)
        lot.save()
        lot = ShipmentLoadingLotAssay(shipment_assay=assay, lot=2, wmt=5087.897, moisture=30.67, ni=1.40)
        lot.save()
        lot = ShipmentLoadingLotAssay(shipment_assay=assay, lot=3, wmt=5087.897, moisture=30.54, ni=1.42)
        lot.save()
        lot = ShipmentLoadingLotAssay(shipment_assay=assay, lot=4, wmt=5087.897, moisture=29.94, ni=1.60)
        lot.save()
        lot = ShipmentLoadingLotAssay(shipment_assay=assay, lot=5, wmt=5087.897, moisture=30.26, ni=1.57)
        lot.save()
        lot = ShipmentLoadingLotAssay(shipment_assay=assay, lot=6, wmt=5087.897, moisture=30.87, ni=1.59)
        lot.save()
        lot = ShipmentLoadingLotAssay(shipment_assay=assay, lot=7, wmt=5087.897, moisture=30.83, ni=1.59)
        lot.save()
        lot = ShipmentLoadingLotAssay(shipment_assay=assay, lot=8, wmt=5087.897, moisture=31.39, ni=1.61)
        lot.save()
        lot = ShipmentLoadingLotAssay(shipment_assay=assay, lot=9, wmt=5087.897, moisture=30.88, ni=1.58)
        lot.save()
        lot = ShipmentLoadingLotAssay(shipment_assay=assay, lot=10, wmt=5087.897, moisture=30.93, ni=1.57)
        lot.save()
        lot = ShipmentLoadingLotAssay(shipment_assay=assay, lot=11, wmt=5087.897, moisture=31.82, ni=1.62)
        lot.save()
        lot = ShipmentLoadingLotAssay(shipment_assay=assay, lot=12, wmt=3413.133, moisture=31.63, ni=1.64)
        lot.save()
        assay.refresh_from_db()

        self.assertEqual(float(assay.bc()), 0.77)
        self.assertEqual(float(assay.dmt), 41058.559)
        self.assertEqual(float(assay.moisture), 30.85)
        self.assertEqual(float(assay.ni), 1.55)
        self.assertEqual(assay.wmt, 59380)
