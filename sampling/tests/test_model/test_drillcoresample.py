from django.core.exceptions import ValidationError
from django.test import TestCase

from sampling.models.proxy import DrillCore
from location.models.source import DrillHole

# pylint: disable=no-member

class DrillCoreTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        drillhole = DrillHole(name='MyHole')
        drillhole.save()

    def setUp(self):
        pass

    def test_core_dont_overlap(self):
        drillhole = DrillHole.objects.all().first()

        core = DrillCore(drill_hole=drillhole,
                         interval_from=0,
                         interval_to=1.5)
        core.save()

        core = DrillCore(drill_hole=drillhole,
                         interval_from=1.4,
                         interval_to=2)
        self.assertRaises(ValidationError, core.clean)

        core = DrillCore(drill_hole=drillhole,
                         interval_from=1.5,
                         interval_to=2.5)
        self.assertEqual(core.clean(), None)
