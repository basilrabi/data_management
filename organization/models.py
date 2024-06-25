from datetime import date
from django.db.models import  (
    BooleanField,
    CharField,
    F,
    ForeignKey,
    Model,
    PROTECT,
    Sum
)

from custom.fields import NameField
from custom.functions_standalone import balance_int
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
    resource_code = NameField(
        blank=True,
        help_text='A single letter used for equipment code assignment for SAP resources.',
        max_length=1,
        null=True,
        unique=True
    )
    service = CharField(blank=False, choices=service_choice, max_length=30, null=True)
    warehouse_code = NameField(blank=True, max_length=3, null=True, unique=True)


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

    def count_equipment(self, equipment_class: str, year: int = None) -> int:
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

    def count_equipment_required(self, equipment_class: str, year: int = None) -> int:
        """
        Given an equipment_class and a year, return the count of equipment required.
        """
        if not year:
            year = date.today().year
        requirement = self.providerequipmentrequirement_set.filter(year=year)
        if requirement.exists():
            quantity = requirement[0].providerequipmentrequirementdetail_set.filter(equipment__name=equipment_class)
            if quantity.exists():
                return quantity.aggregate(Sum('with_spare'))['with_spare__sum']
        return 0

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
        ad_req = self.count_equipment_required('AD', year)
        ct_req = self.count_equipment_required('CT', year)
        dt_req = self.count_equipment_required('DT', year)
        ft_req = self.count_equipment_required('FT', year)
        rg_req = self.count_equipment_required('RG', year)
        st_req = self.count_equipment_required('ST', year)
        sv_req = self.count_equipment_required('SV', year)
        tl_req = self.count_equipment_required('TL', year)
        tx_req = self.count_equipment_required('TX', year)
        vr_req = self.count_equipment_required('VR', year)
        wl_req = self.count_equipment_required('WL', year)
        wt_req = self.count_equipment_required('WT', year)
        total_req = ad_req + ct_req + dt_req + ft_req + rg_req + st_req + sv_req + tl_req + tx_req + vr_req + wl_req + wt_req
        ad_bal = balance_int(ad_req, ad)
        ct_bal = balance_int(ct_req, ct)
        dt_bal = balance_int(dt_req, dt)
        ft_bal = balance_int(ft_req, ft)
        rg_bal = balance_int(rg_req, rg)
        st_bal = balance_int(st_req, st)
        sv_bal = balance_int(sv_req, sv)
        tl_bal = balance_int(tl_req, tl)
        tx_bal = balance_int(tx_req, tx)
        vr_bal = balance_int(vr_req, vr)
        wl_bal = balance_int(wl_req, wl)
        wt_bal = balance_int(wt_req, wt)
        total_bal = ad_bal + ct_bal + dt_bal + ft_bal + rg_bal + st_bal + sv_bal + tl_bal + tx_bal + vr_bal + wl_bal + wt_bal
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
            'Total': total,
            'AD_req': ad_req,
            'CT_req': ct_req,
            'DT_req': dt_req,
            'FT_req': ft_req,
            'RG_req': rg_req,
            'ST_req': st_req,
            'SV_req': sv_req,
            'TL_req': tl_req,
            'TX_req': tx_req,
            'VR_req': vr_req,
            'WL_req': wl_req,
            'WT_req': wt_req,
            'Total_req': total_req,
            'AD_bal': ad_bal,
            'CT_bal': ct_bal,
            'DT_bal': dt_bal,
            'FT_bal': ft_bal,
            'RG_bal': rg_bal,
            'ST_bal': st_bal,
            'SV_bal': sv_bal,
            'TL_bal': tl_bal,
            'TX_bal': tx_bal,
            'VR_bal': vr_bal,
            'WL_bal': wl_bal,
            'WT_bal': wt_bal,
            'Total_bal': total_bal
        }


class Section(Model):
    name = CharField(max_length=30, null=True, blank=False, unique=True)
    parent_department = ForeignKey('Department', on_delete=PROTECT)

