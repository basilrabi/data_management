from django.core.exceptions import ValidationError
from django.test import TestCase

from shipment.models.lct import LCT, LCTContract

# pylint: disable=no-member

class  LCTContractTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        lct = LCT(name='guagua', capacity=1000)
        lct.save()

    def setUp(self):
        pass

    def test_end_is_valid(self):
        lct = LCT.objects.all().first()
        lct_contract = LCTContract(
            lct=lct, start='2019-08-17', end='2019-08-19'
        )
        self.assertEqual(lct_contract.clean(), None)
        lct_contract.save()

        self.assertEqual(lct_contract.start, '2019-08-17')
        self.assertEqual(lct_contract.end, '2019-08-19')

        lct_contract = LCTContract(
            lct=lct, start='2019-08-16', end='2019-08-14'
        )
        self.assertRaises(ValidationError, lct_contract.clean)

    def test_contract_do_not_overlap(self):
        lct = LCT.objects.all().first()
        lct_contract = LCTContract(
            lct = lct, start = '2019-08-17', end = '2019-08-19'
        )
        lct_contract.save()

        lct_contract = LCTContract(
            lct = lct, start = '2019-08-19', end = '2019-08-21'
        )
        self.assertRaises(ValidationError, lct_contract.clean)

        lct_contract = LCTContract(
            lct = lct, start = '2019-08-14', end = '2019-08-17'
        )
        self.assertRaises(ValidationError, lct_contract.clean)

        lct_contract = LCTContract(
            lct = lct, start = '2019-08-20', end = '2019-08-21'
        )
        self.assertEqual(lct_contract.clean(), None)

        lct_contract = LCTContract(
            lct = lct, start = '2019-08-14', end = '2019-08-16'
        )
        self.assertEqual(lct_contract.clean(), None)
