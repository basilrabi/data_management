from django.test import TestCase

from custom.functions import sms_response, setup_triggers
from custom.models import MobileNumber, User
from fleet.models.equipment import (
    Equipment,
    EquipmentClass,
    EquipmentManufacturer,
    EquipmentModel
)
from organization.models import Organization


class SmsResponseTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        setup_triggers()

    def setUp(self):
        org = Organization(name="TMC")
        org.save()
        org.refresh_from_db()
        user = User(username='username',
                    first_name='developer',
                    last_name='taganito')
        user.save()
        user.refresh_from_db()
        MobileNumber(user=user, number='+639771358478').save()
        equipment_class = EquipmentClass(name='DT')
        equipment_class.save()
        equipment_class.refresh_from_db()
        manufacturer = EquipmentManufacturer(name='VOLVO')
        manufacturer.save()
        manufacturer.refresh_from_db()
        model = EquipmentModel(equipment_class=equipment_class,
                               manufacturer=manufacturer,
                               name='FMX440')
        model.save()
        model.refresh_from_db()
        equipment = Equipment(fleet_number=101,
                              model=model,
                              owner=org)
        equipment.save()

    def test_sms_response(self):
        user = User.objects.get(first_name='developer')
        self.assertEqual(
            sms_response('XXX', user)[:26],
            'Text pattern unrecognized.'
        )
        self.assertEqual(
            sms_response('DTT 128 1.1 1.1', user)[:36],
            'Equipment type "DTT" does not exist.'
        )
        self.assertEqual(
            sms_response('DT 128 1.1 1.1', user)[:33],
            'TMC DT 128 is not yet registered.'
        )
        self.assertEqual(
            sms_response('DT 101 125.7383 9.5803', user)[:17],
            'Invalid location.'
        )
        self.assertEqual(
            sms_response('DT 101 125.8246 9.5176', user)[:14],
            'Location saved'
        )
        self.assertEqual(
            sms_response('TMCc DTT 128 1.1 1.1', user)[:30],
            'Company "TMCC" does not exist.'
        )
        self.assertEqual(
            sms_response('TMC DTT 128 1.1 1.1', user)[:36],
            'Equipment type "DTT" does not exist.'
        )
        self.assertEqual(
            sms_response('TMC DT 128 1.1 1.1', user)[:33],
            'TMC DT 128 is not yet registered.'
        )
        self.assertEqual(
            sms_response('TMC DT 101 125.7383 9.5803', user)[:17],
            'Invalid location.'
        )
        self.assertEqual(
            sms_response('TMC DT 101 125.8246 9.5176', user)[:14],
            'Location saved'
        )
