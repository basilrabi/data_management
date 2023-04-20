from django.db.models import (
    CharField,
    DateField,
    ForeignKey,
    F,
    IntegerField,
    Model,
    PositiveSmallIntegerField,
    PROTECT,
    SET_NULL,
    UniqueConstraint
)
from django.utils.dateformat import MONTHS

from custom.fields import AlphaNumeric, NameField
from custom.models import Classification, FixedAsset
from organization.models import Department, Division, Organization, Section


class BodyType(Classification):
    class Meta:
        ordering = [F('name').asc()]


class Equipment(FixedAsset):
    """
    A single piece of equipment.
    """

    def DeptChoices():
        dept_choices = list(Department.objects.values_list('name', 'name'))
        div_choices = list(Division.objects.values_list('name', 'name'))
        sec_choices = list(Section.objects.values_list('name', 'name'))

        return dept_choices + div_choices + sec_choices

    MONTH_CHOICES = [(month_num, month_name) for month_num, month_name in MONTHS.items()]

    owner = ForeignKey(Organization, on_delete=PROTECT)
    department_assigned = CharField(max_length=30, choices=tuple(DeptChoices()), null=True, blank=True)
    fleet_number = PositiveSmallIntegerField()
    model = ForeignKey('EquipmentModel', on_delete=PROTECT)
    body_type = ForeignKey('BodyType', on_delete=PROTECT, null=True, blank=True)
    year_model = IntegerField(null = True, blank=True)
    certificate_of_registration_no = CharField(max_length=30, null = True, blank=True)
    cr_date = DateField(null = True, blank=True)
    mv_file_no = CharField(max_length=30, null = True, blank=True)
    engine_serial_number = AlphaNumeric(max_length=100, null=True, blank=True)
    plate_number = NameField(max_length=20, null = True, blank = True)
    month_of_registration = CharField(max_length=20, null=True, blank=True, choices=MONTH_CHOICES, help_text="Based on plate number")
    chassis_serial_number = NameField(max_length=100, null = True, blank = True)
    
    equipment_class = ForeignKey(
        'EquipmentClass', on_delete=SET_NULL, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        self.equipment_class = self.model.equipment_class
        super().save(*args, **kwargs)

    class Meta:
        constraints = [UniqueConstraint(
            fields=['fleet_number', 'equipment_class', 'owner'],
            name='unique_equipment_constraint'
        )]
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipment'
        ordering = [
            F('owner__name').asc(),
            F('equipment_class__name').asc(),
            F('fleet_number').asc(),
        ]

    def __str__(self):
        return f'{self.owner} {self.equipment_class.name}-{self.fleet_number}'


class EquipmentClass(Classification):

    class Meta:
        verbose_name = 'Equipment Class'
        verbose_name_plural = 'Equipment Classes'
        ordering = [F('name').asc()]

    def __str__(self):
        return f'{self.name} - {self.description}'


class EquipmentManufacturer(Classification):

    class Meta:
        ordering = [F('name').asc()]


class EquipmentModel(Classification):
    name = NameField(max_length=40)
    equipment_class = ForeignKey('EquipmentClass', on_delete=PROTECT)
    manufacturer = ForeignKey('EquipmentManufacturer', on_delete=PROTECT)

    class Meta:
        constraints = [UniqueConstraint(
            fields=['name', 'equipment_class', 'manufacturer'],
            name='unique_equipment_model_constraint'
        )]
        ordering = [
            F('manufacturer__name').asc(),
            F('equipment_class__name').asc(),
            F('name').asc()
        ]

    def __str__(self):
        return f'{self.equipment_class.name} - {self.manufacturer.name} {self.name}'


class TrackedExcavator(Model):
    fleet_number = PositiveSmallIntegerField(unique=True)

    class Meta:
        ordering = ['fleet_number']

    def __str__(self):
        return f'TX-{self.fleet_number}'
