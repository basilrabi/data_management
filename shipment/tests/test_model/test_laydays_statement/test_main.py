from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.dateparse import parse_datetime as pdt

from shipment.models.dso import (LayDaysStatement,
                                 Shipment,
                                 Vessel)

# pylint: disable=no-member

class  LayDaysStatementTest(TestCase):

    def setUp(self):
        vessel = Vessel(name='Chang Shun II')
        vessel.save()
        shipment = Shipment(name='431-C', vessel=vessel)
        shipment.save()

    def test_arrival_at_tmc_should_be_later_than_arrival_at_surigao(self):
        shipment = Shipment.objects.all().first()
        statement = LayDaysStatement(
            shipment=shipment,
            arrival_pilot=pdt('2019-08-16 12:00:00+0800'),
            arrival_tmc=pdt('2019-08-16 00:00:00+0800')
        )
        self.assertRaises(ValidationError, statement.clean)
        statement = LayDaysStatement(
            shipment=shipment,
            arrival_pilot=pdt('2019-08-16 00:00:00+0800'),
            arrival_tmc=pdt('2019-08-16 12:00:00+0800')
        )
        self.assertEqual(statement.clean(), None)

    def test_cannot_accept_without_vessel(self):
        shipment = Shipment.objects.all().first()
        shipment.vessel = None
        shipment.save()
        statement = LayDaysStatement(
            shipment=shipment,
            arrival_pilot=pdt('2019-08-16 00:00:00+0800'),
            arrival_tmc=pdt('2019-08-16 12:00:00+0800')
        )
        self.assertRaises(ValidationError, statement.clean)

    def test_nor_tender_should_be_later_than_acceptance(self):
        shipment = Shipment.objects.all().first()
        statement = LayDaysStatement(
            shipment=shipment,
            nor_tender=pdt('2019-08-16 12:00:00+0800'),
            nor_accepted=pdt('2019-08-16 00:00:00+0800')
        )
        self.assertRaises(ValidationError, statement.clean)
        statement = LayDaysStatement(
            shipment=shipment,
            nor_tender=pdt('2019-08-16 00:00:00+0800'),
            nor_accepted=pdt('2019-08-16 12:00:00+0800')
        )
        self.assertEqual(statement.clean(), None)

    def test_nor_tender_not_earlier_than_arrival_at_tmc(self):
        shipment = Shipment.objects.all().first()
        statement = LayDaysStatement(
            shipment=shipment,
            arrival_tmc=pdt('2019-08-16 12:00:00+0800'),
            nor_tender=pdt('2019-08-16 00:00:00+0800')
        )
        self.assertRaises(ValidationError, statement.clean)
        statement = LayDaysStatement(
            shipment=shipment,
            arrival_tmc=pdt('2019-08-16 00:00:00+0800'),
            nor_tender=pdt('2019-08-16 00:00:00+0800')
        )
        self.assertEqual(statement.clean(), None)
