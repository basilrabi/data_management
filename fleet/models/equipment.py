from django.db.models import (
    BooleanField,
    DateField,
    DecimalField,
    F,
    Model,
    ForeignKey,
    PositiveSmallIntegerField,
    PROTECT,
    SET_NULL,
    UniqueConstraint
)

from custom.models import Classification
from custom.fields import AlphaNumeric, NameField
from organization.models import Organization

class Equipment(Model):
    """
    A single piece of equipment.
    """
    fleet_number = PositiveSmallIntegerField()
    model = ForeignKey('EquipmentModel', on_delete=PROTECT)
    owner = ForeignKey(Organization, on_delete=PROTECT)
    acquisition_cost = DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2,
        help_text='Cost in Philippine Peso as recorded by TSD'
    )
    acquisition_cost_from_accounting = DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2,
        help_text='Cost in Philippine Peso'
    )
    date_acquired = DateField(null=True, blank=True)
    date_phased_out = DateField(null=True, blank=True)
    engine_serial_number = AlphaNumeric(max_length=100, null=True, blank=True)
    plate_number = NameField(max_length=20, null = True, blank = True)
    chassis_serial_number = NameField(max_length=100, null = True, blank = True)
    active = BooleanField(default=True)

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
            F('fleet_number').asc()
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
