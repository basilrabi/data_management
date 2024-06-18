from datetime import date
from django.db.models import  (
    BooleanField,
    CharField,
    F,
    ForeignKey,
    Model,
    PROTECT
)

from custom.fields import NameField
from custom.models import Classification


class Department(Model):
    name = CharField(max_length=30, null=True, blank=False, unique=True)
    abbreviation = CharField(max_length=10, null=True, blank=False)
    parent_division = ForeignKey('Division', on_delete=PROTECT)


class Division(Model):
    name = CharField(max_length=30, null=True, blank=False, unique=True)
    abbreviation = CharField(max_length=10, null=True, blank=False)

    def __str__(self):
        return self.name


class ManilaGpsApiKey(Model):
    owner = ForeignKey('Organization', on_delete=PROTECT)
    key = CharField(max_length=60, unique=True)

    class Meta:
        ordering = [
            F('owner__name').asc(),
            F('key').asc()
        ]

    def __str__(self):
        return f'{self.owner} : {self.key}'


class Organization(Classification):

    service_choice = (
        ('Contractor', 'Contractor'),
        ('Operating Company', 'OpCo'),
        ('Government Agency', 'Govt')
    )

    active = BooleanField(default=True)
    service = CharField(blank=False, choices=service_choice, max_length=30, null=True)
    warehouse_code = NameField(blank=True, max_length=3, null=True)


class OrganizationUnit(Model):
    """
    Table containing all organization units
    """
    uid = CharField(max_length=15, unique=True)
    name = CharField(max_length=30)
    abbreviation = CharField(max_length=30)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class ServiceProvider(Organization):
    """
    Service contractors
    """

    def save(self, *args, **kwargs):
        self.service = 'Contractor'
        super().save(*args, **kwargs)

    class Meta:
        proxy = True

    def count_equipment(self, equipment_class, year=None) -> int:
        """
        Given an equipment_class and a year, return the count of equipment in the registry.
        """
        if not year:
            year = date.today().year
        units = self.equipment_set.filter(equipment_class__name=equipment_class)
        count = 0
        if units.count() > 0:
            for unit in units:
                try:
                    if unit.providerequipmentregistry_set.filter(year=year, pull_out_date__isnull=True).exists():
                        count += 1
                except ValueError:
                    pass
        return count

    def equipment_registry_count(self, year=None) -> dict:
        ad = self.count_equipment('AD', year)
        ct = self.count_equipment('CT', year)
        dt = self.count_equipment('DT', year)
        ft = self.count_equipment('FT', year)
        rg = self.count_equipment('RG', year)
        st = self.count_equipment('ST', year)
        sv = self.count_equipment('SV', year)
        tl = self.count_equipment('TL', year)
        tx = self.count_equipment('TX', year)
        vr = self.count_equipment('VR', year)
        wl = self.count_equipment('WL', year)
        wt = self.count_equipment('WT', year)
        total = ad + ct + dt + ft + rg + st + sv + tl + tx + vr + wl + wt
        return {
            'contractor': self.__str__(),
            'AD': ad,
            'CT': ct,
            'DT': dt,
            'FT': ft,
            'RG': rg,
            'ST': st,
            'SV': sv,
            'TL': tl,
            'TX': tx,
            'VR': vr,
            'WL': wl,
            'WT': wt,
            'Total': total
        }


class Section(Model):
    name = CharField(max_length=30, null=True, blank=False, unique=True)
    parent_department = ForeignKey('Department', on_delete=PROTECT)

