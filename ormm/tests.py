from datetime import date
from django.test import TestCase

from .models import ExternalCommunication


class ExternalCommunicationTest(TestCase):

    def setUp(self):
        pass

    def test_entry_after_deletion(self):
        date_test = date(2023, 5, 22)
        first_entry = ExternalCommunication(date=date_test, nature_of_content="First entry test")
        first_entry.save()

        second_entry = ExternalCommunication(date=date_test, nature_of_content="Second entry test")
        second_entry.save()
        second_entry.delete()

        third_entry = ExternalCommunication(date=date_test, nature_of_content="Third entry test")
        third_entry.save()

        test_transmittal = third_entry.transmittal_number
        self.assertEqual(test_transmittal, 'ORMM-002-2023')
