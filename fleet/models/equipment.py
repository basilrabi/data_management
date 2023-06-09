from django.core.exceptions import ValidationError
from django.db.models import (
    CharField,
    DateField,
    ForeignKey,
    F,
    Model,
    PositiveSmallIntegerField,
    PROTECT,
    SET_NULL,
    UniqueConstraint
)

from custom.fields import AlphaNumeric, NameField
from custom.functions_standalone import month_choices
from custom.models import Classification, FixedAsset
from organization.models import Organization, OrganizationUnit


class AdditionalEquipmentCost(FixedAsset):
    """
    Additional Capitalized Expenses for Equipment
    """
    equipment = ForeignKey('Equipment', on_delete=PROTECT)


class BodyType(Classification):
    class Meta:
        ordering = [F('name').asc()]


class Equipment(FixedAsset):
    """
    A single piece of equipment.
    """
    owner = ForeignKey(Organization, on_delete=PROTECT)
    department_assigned = ForeignKey(
        OrganizationUnit, on_delete=SET_NULL, null=True, blank=True
    )
    fleet_number = PositiveSmallIntegerField()
    model = ForeignKey('EquipmentModel', on_delete=PROTECT)
    body_type = ForeignKey('BodyType', on_delete=PROTECT, null=True, blank=True)
    year_model = PositiveSmallIntegerField(null = True, blank=True)
    certificate_of_registration_no = CharField(
        max_length=30, null = True, blank=True
    )
    cr_date = DateField(null = True, blank=True)
    mv_file_no = CharField(max_length=30, null = True, blank=True)
    engine_serial_number = AlphaNumeric(max_length=100, null=True, blank=True)
    plate_number = NameField(max_length=20, null = True, blank = True)
    month_of_registration = CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=month_choices(),
        help_text="Based on plate number"
    )
    chassis_serial_number = NameField(max_length=100, null = True, blank = True)

    equipment_class = ForeignKey(
        'EquipmentClass', on_delete=SET_NULL, null=True, blank=True
    )

    def clean(self) -> None:
        super().clean()
        try:
            error = f'{self.owner}-{self.model.equipment_class.name}-{self.fleet_number:03d} already exists.'
            if self.id:
                if Equipment.objects.filter(
                    fleet_number=self.fleet_number,
                    owner=self.owner,
                    equipment_class=self.model.equipment_class
                ).exclude(id=self.id).exists():
                    raise ValidationError(error)
            else:
                if Equipment.objects.filter(
                    fleet_number=self.fleet_number,
                    owner=self.owner,
                    equipment_class=self.model.equipment_class
                ).exists():
                    raise ValidationError(error)
        except:
            pass

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
        if self.date_acquired:
            year = str(self.date_acquired.year)[2:4]
        else:
            year = "00"
        return f'{self.owner}-{self.equipment_class.name}{year}-{self.fleet_number:03d}'


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
