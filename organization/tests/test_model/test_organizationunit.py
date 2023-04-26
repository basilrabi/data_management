from django.test import TestCase

from custom.functions import setup_triggers
from organization.models import (
    Department,
    Division,
    OrganizationUnit,
    Section
)


class OrganizationUnitTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        setup_triggers()

    def setUp(self):
        pass

    def test_trigger_works(self):
        # Inserting organization units

        source_div = Division(name='Div A', abbreviation='DivA')
        source_div.save()
        source_div.refresh_from_db()
        div = OrganizationUnit.objects.filter(name='Div A')
        self.assertEqual(div.exists(), True)
        div = div.first()
        self.assertEqual(div.uid, f'division{source_div.id}')
        self.assertEqual(div.abbreviation, source_div.abbreviation)
        self.assertEqual(div.name, source_div.name)

        source_dep = Department(
            name='Dep A', abbreviation='DepA', parent_division=source_div
        )
        source_dep.save()
        source_dep.refresh_from_db()
        dep = OrganizationUnit.objects.filter(name='Dep A')
        self.assertEqual(dep.exists(), True)
        dep = dep.first()
        self.assertEqual(dep.uid, f'department{source_dep.id}')
        self.assertEqual(dep.abbreviation, source_dep.abbreviation)
        self.assertEqual(dep.name, source_dep.name)

        source_sec = Section(name='Sec A', parent_department=source_dep)
        source_sec.save()
        source_sec.refresh_from_db()
        sec = OrganizationUnit.objects.filter(name='Sec A')
        self.assertEqual(sec.exists(), True)
        sec = sec.first()
        self.assertEqual(sec.uid, f'section{source_sec.id}')
        self.assertEqual(sec.abbreviation, source_sec.name)
        self.assertEqual(sec.name, source_sec.name)

        # Adding independent units
        ind_div = Division(name='Independent A', abbreviation='Ind')
        ind_div.save()
        ind_div.refresh_from_db()
        count = OrganizationUnit.objects.all().count()
        self.assertEqual(count, 3)
        Department(
            name='Independent A',
            abbreviation='Ind B',
            parent_division=ind_div
        ).save()
        count = OrganizationUnit.objects.all().count()
        self.assertEqual(count, 3)

        # Updating units

        source_div.name = 'Division A'
        source_div.abbreviation = 'DA'
        source_div.save()
        source_div.refresh_from_db()
        div = OrganizationUnit.objects.filter(name='Division A').first()
        self.assertEqual(div.uid, f'division{source_div.id}')
        self.assertEqual(div.abbreviation, source_div.abbreviation)
        self.assertEqual(div.name, source_div.name)

        source_dep.name = 'Department A'
        source_dep.abbreviation = 'DEA'
        source_dep.save()
        source_dep.refresh_from_db()
        dep = OrganizationUnit.objects.filter(name='Department A').first()
        self.assertEqual(dep.uid, f'department{source_dep.id}')
        self.assertEqual(dep.abbreviation, source_dep.abbreviation)
        self.assertEqual(dep.name, source_dep.name)

        source_sec.name = 'Section A'
        source_sec.save()
        source_sec.refresh_from_db()
        sec = OrganizationUnit.objects.filter(name='Section A').first()
        self.assertEqual(sec.uid, f'section{source_sec.id}')
        self.assertEqual(sec.abbreviation, source_sec.name)
        self.assertEqual(sec.name, source_sec.name)

        source_div = Division.objects.get(name='Independent A')
        source_div.name = 'Division B'
        source_div.abbreviation = 'DB'
        source_div.save()
        count = OrganizationUnit.objects.all().count()
        self.assertEqual(count, 4)
        source_div = Division.objects.get(name='Division B')
        source_div.name = 'Independent A'
        source_div.save()
        count = OrganizationUnit.objects.all().count()
        self.assertEqual(count, 3)

        # Deletion
        Section.objects.get(name='Section A').delete()
        Department.objects.get(name='Department A').delete()
        Division.objects.get(name='Division A').delete()
        count = OrganizationUnit.objects.all().count()
        self.assertEqual(count, 0)
