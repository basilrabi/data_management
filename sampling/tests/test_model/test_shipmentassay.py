from decimal import Decimal
from django.core.exceptions import ValidationError
from django.test import TestCase

from custom.functions import setup_triggers
from sampling.models.proxy import ChinaShipmentAssay, PamcoShipmentAssay
from sampling.models.sample import (
    Laboratory,
    ShipmentDischargeLotAssay,
    ShipmentLoadingAssay,
    ShipmentLoadingLotAssay
)
from shipment.models.dso import Destination, Product, Shipment, Vessel


class ChinaShipmentAssayTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        setup_triggers()

    def setUp(self):
        vessel = Vessel(name='Aqua Atlantic')
        vessel.save()
        shipment = Shipment(name='460-C', vessel=vessel)
        shipment.save()
        laboratory = Laboratory(name='Intertek')
        laboratory.save()

    def test_dmt_trigger(self):
        shipment = Shipment.objects.first()
        laboratory = Laboratory.objects.first()
        assay = ChinaShipmentAssay(laboratory=laboratory,
                                   shipment=shipment,
                                   ni=1.43,
                                   fe=14.4,
                                   sio2=35.38,
                                   mgo=27.43,
                                   p=0.0021,
                                   al2o3=0.9,
                                   s=0.007,
                                   cao=0.046,
                                   wmt=53649,
                                   moisture=29.92)
        assay.save()
        assay.refresh_from_db()

        self.assertEqual(float(assay.dmt), 37597.219)

        assay.wmt = assay.dmt
        self.assertRaises(ValidationError, assay.clean)
        assay.wmt = assay.dmt - Decimal(0.001)
        self.assertRaises(ValidationError, assay.clean)

    def test_moisture_trigger(self):
        shipment = Shipment.objects.first()
        laboratory = Laboratory.objects.first()
        assay = ChinaShipmentAssay(laboratory=laboratory,
                                   shipment=shipment,
                                   ni=1.43,
                                   fe=14.4,
                                   sio2=35.38,
                                   mgo=27.43,
                                   p=0.0021,
                                   al2o3=0.9,
                                   s=0.007,
                                   cao=0.046,
                                   wmt=53649,
                                   dmt=37597.219)
        assay.save()
        assay.refresh_from_db()

        self.assertEqual(float(assay.moisture), 29.92)

        # Approval
        approval = assay.approvedshipmentdischargeassay
        approval.approved = True
        approval.save()

        self.assertRaises(ValidationError, assay.clean)


class PamcoShipmentAssayTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        setup_triggers()

    def setUp(self):
        lab = Laboratory(name='PAMCO')
        lab.save()
        vessel = Vessel(name='New Beginning')
        vessel.save()
        shipment = Shipment(name='282', vessel=vessel)
        shipment.save()

    def test_correct_computation(self):
        shipment = Shipment.objects.first()
        assay = PamcoShipmentAssay(shipment=shipment,
                                   co=0.07,
                                   cr=0.92,
                                   mn=0.30,
                                   fe=16.49,
                                   sio2=33.7,
                                   cao=0.02,
                                   mgo=25.38,
                                   al2o3=0.93,
                                   p=0.0004,
                                   s=0.015,
                                   ignition_loss=12.26)
        assay.save()
        lot = ShipmentDischargeLotAssay(
            shipment_assay=assay, lot=1, wmt=4901.5, moisture=32.92, ni=1.73
        )
        lot.save()
        lot = ShipmentDischargeLotAssay(
            shipment_assay=assay, lot=2, wmt=4901.5, moisture=32.99, ni=1.71
        )
        lot.save()
        lot = ShipmentDischargeLotAssay(
            shipment_assay=assay, lot=3, wmt=4901.5, moisture=33.21, ni=1.71
        )
        lot.save()
        lot = ShipmentDischargeLotAssay(
            shipment_assay=assay, lot=4, wmt=4901.5, moisture=33.12, ni=1.73
        )
        lot.save()
        lot = ShipmentDischargeLotAssay(
            shipment_assay=assay, lot=5, wmt=4901.5, moisture=32.96, ni=1.73
        )
        lot.save()
        lot = ShipmentDischargeLotAssay(
            shipment_assay=assay, lot=6, wmt=4901.5, moisture=32.90, ni=1.74
        )
        lot.save()
        lot = ShipmentDischargeLotAssay(
            shipment_assay=assay, lot=7, wmt=4901.5, moisture=31.46, ni=1.76
        )
        lot.save()
        lot = ShipmentDischargeLotAssay(
            shipment_assay=assay, lot=8, wmt=4901.5, moisture=32.10, ni=1.75
        )
        lot.save()
        lot = ShipmentDischargeLotAssay(
            shipment_assay=assay, lot=9, wmt=4901.5, moisture=32.73, ni=1.76
        )
        lot.save()
        lot = ShipmentDischargeLotAssay(
            shipment_assay=assay, lot=10, wmt=4901.5, moisture=32.60, ni=1.75
        )
        lot.save()
        assay.refresh_from_db()

        self.assertEqual(float(assay.bc()), 0.75)
        self.assertEqual(float(assay.dmt), 32987.586)
        self.assertEqual(float(assay.moisture), 32.7)
        self.assertEqual(float(assay.ni), 1.74)
        self.assertEqual(assay.laboratory.name, 'PAMCO')
        self.assertEqual(assay.wmt, 49015)

        # Approval
        approval = assay.approvedshipmentdischargeassay
        approval.approved = True
        approval.save()

        self.assertRaises(ValidationError, assay.clean)


class ShipmentLoadingAssayTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        setup_triggers()

    def setUp(self):
        destination = Destination(name='A')
        destination.save()
        destination = Destination(name='B')
        destination.save()
        product = Product(name='TYPE A')
        product.save()
        product = Product(name='TYPE B')
        product.save()
        vessel = Vessel(name='Fakku')
        vessel.save()
        vessel = Vessel(name='Jin Hong')
        vessel.save()
        shipment = Shipment(name='481-C',
                            vessel=vessel,
                            product=product,
                            destination=destination)
        shipment.save()

    def test_correct_computation(self):
        shipment = Shipment.objects.first()
        assay = ShipmentLoadingAssay(date='2020-07-29',
                                     shipment=shipment,
                                     fe=16.02,
                                     mgo=26.49,
                                     sio2=34.24,
                                     cr=0.86)
        assay.save()
        lot = ShipmentLoadingLotAssay(
            shipment_assay=assay, lot=1, wmt=5087.897, moisture=30.75, ni=1.44
        )
        lot.save()
        lot = ShipmentLoadingLotAssay(
            shipment_assay=assay, lot=2, wmt=5087.897, moisture=30.67, ni=1.40
        )
        lot.save()
        lot = ShipmentLoadingLotAssay(
            shipment_assay=assay, lot=3, wmt=5087.897, moisture=30.54, ni=1.42
        )
        lot.save()
        lot = ShipmentLoadingLotAssay(
            shipment_assay=assay, lot=4, wmt=5087.897, moisture=29.94, ni=1.60
        )
        lot.save()
        lot = ShipmentLoadingLotAssay(
            shipment_assay=assay, lot=5, wmt=5087.897, moisture=30.26, ni=1.57
        )
        lot.save()
        lot = ShipmentLoadingLotAssay(
            shipment_assay=assay, lot=6, wmt=5087.897, moisture=30.87, ni=1.59
        )
        lot.save()
        lot = ShipmentLoadingLotAssay(
            shipment_assay=assay, lot=7, wmt=5087.897, moisture=30.83, ni=1.59
        )
        lot.save()
        lot = ShipmentLoadingLotAssay(
            shipment_assay=assay, lot=8, wmt=5087.897, moisture=31.39, ni=1.61
        )
        lot.save()
        lot = ShipmentLoadingLotAssay(
            shipment_assay=assay, lot=9, wmt=5087.897, moisture=30.88, ni=1.58
        )
        lot.save()
        lot = ShipmentLoadingLotAssay(
            shipment_assay=assay, lot=10, wmt=5087.897, moisture=30.93, ni=1.57
        )
        lot.save()
        lot = ShipmentLoadingLotAssay(
            shipment_assay=assay, lot=11, wmt=5087.897, moisture=31.82, ni=1.62
        )
        lot.save()
        lot = ShipmentLoadingLotAssay(
            shipment_assay=assay, lot=12, wmt=3413.133, moisture=31.63, ni=1.64
        )
        lot.save()
        assay.refresh_from_db()
        approval = assay.approvedshipmentloadingassay

        self.assertEqual(assay.clean(), None)
        self.assertEqual(round(float(assay.bc()), 2), 0.77)
        self.assertEqual(float(assay.dmt), 41058.559)
        self.assertEqual(float(assay.moisture), 30.85)
        self.assertEqual(float(assay.ni), 1.55)
        self.assertEqual(assay.wmt, 59380)

        approval.approved = True
        approval.save()
        assay.refresh_from_db()
        self.assertRaises(ValidationError, assay.clean)

        self.assertEqual(shipment.clean(), None)
        product_new = Product.objects.get(name='Type A')
        shipment.product = product_new
        self.assertRaises(ValidationError, shipment.clean)

        product_new = Product.objects.get(name='Type B')
        shipment.product = product_new
        self.assertEqual(shipment.clean(), None)

        destination_new = Destination.objects.get(name='A')
        shipment.destination = destination_new
        self.assertRaises(ValidationError, shipment.clean)

        destination_new = Destination.objects.get(name='B')
        shipment.destination = destination_new
        self.assertEqual(shipment.clean(), None)

        vessel_new = Vessel.objects.get(name='FAKKU')
        shipment.vessel = vessel_new
        self.assertRaises(ValidationError, shipment.clean)
