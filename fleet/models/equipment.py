from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import (
    BooleanField,
    CharField,
    CheckConstraint,
    DateField,
    DateTimeField,
    DecimalField,
    DurationField,
    F,
    ForeignKey,
    Index,
    Model,
    OneToOneField,
    PositiveSmallIntegerField,
    PROTECT,
    Q,
    SET_NULL,
    UniqueConstraint
)
from phonenumber_field.modelfields import PhoneNumberField

from custom.fields import AlphaNumeric, NameField, SpaceLess
from custom.functions_standalone import month_choices
from custom.models import Classification, FixedAsset, UnitOfMeasure
from organization.models import Organization, OrganizationUnit, ServiceProvider
from ..manager import ProviderEquipmentManager


class AdditionalEquipmentCost(FixedAsset):
    """
    Additional Capitalized Expenses for Equipment
    """
    equipment = ForeignKey('Equipment', on_delete=PROTECT)


class BodyType(Classification):
    class Meta:
        ordering = [F('name').asc()]


class Capacity(Model):
    value = DecimalField(max_digits=10, decimal_places=2)
    unit_of_measure = ForeignKey(UnitOfMeasure, on_delete=PROTECT)

    class Meta:
        constraints = [UniqueConstraint(
            fields=['unit_of_measure', 'value'],
            name='unique_equipment_capacity'
        )]
        ordering = [
            F('unit_of_measure__name').asc(),
            F('value').asc()
        ]
        verbose_name_plural = 'Capacities'

    def __str__(self) -> str:
        return f'{self.value:,.2f} {self.unit_of_measure.name}'


class ChassisSerialNumber(Model):
    """
    Serial number used in equipment manufacturing
    """
    name = AlphaNumeric(max_length=100)

    class Meta:
        ordering = [F('name').asc()]

    def __str__(self) -> str:
        return self.name


class EngineSerialNumber(Model):
    """
    Serial number used in equipment manufacturing
    """
    name = AlphaNumeric(max_length=100)

    class Meta:
        ordering = [F('name').asc()]

    def __str__(self) -> str:
        return self.name


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

    def __str__(self) -> str:
        if self.date_acquired:
            year = str(self.date_acquired.year)[2:4]
        else:
            year = "00"
        return f'{self.owner}-{self.equipment_class.name}{year}-{self.fleet_number:03d}'


class EquipmentClass(Classification):

    class Meta:
        indexes = [Index(fields=['name'])]
        ordering = [F('name').asc()]
        verbose_name = 'Equipment Class'
        verbose_name_plural = 'Equipment Classes'

    def __str__(self) -> str:
        return f'{self.name} - {self.description}'


class EquipmentIdlingTime(Model):
    """
    The model to capture equipment idling from Manila GPS.
    """
    equipment = ForeignKey(Equipment, on_delete=PROTECT)
    time_stamp = DateTimeField()
    idling = BooleanField()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['equipment', 'time_stamp'],
                name='unique_equipment_idling_timestamp'
            )
        ]
        indexes = [
            Index(fields=['time_stamp']),
            Index(fields=['idling'])
        ]


class EquipmentIgnitionStatus(Model):
    """
    The model to capture ignition status from Manila GPS.
    """
    equipment = ForeignKey(Equipment, on_delete=PROTECT)
    time_stamp = DateTimeField()
    ignition = BooleanField()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['equipment', 'time_stamp'],
                name='unique_equipment_ignition_timestamp'
            )
        ]
        indexes = [
            Index(fields=['time_stamp']),
            Index(fields=['ignition'])
        ]
        verbose_name_plural = 'equipment ignition statuses'


class EquipmentManufacturer(Classification):

    class Meta:
        ordering = [F('name').asc()]


class EquipmentMobileNumber(Model):
    """
    Mobile number assigned to an equipment for receiving and sending SMS data.
    """
    equipment = OneToOneField(
        Equipment, blank=True, null=True, on_delete=PROTECT
    )
    number = PhoneNumberField(unique=True)
    spaceless_number = SpaceLess(
        blank=True, max_length=20, null=True, unique=True
    )

    def save(self, *args, **kwargs):
        self.spaceless_number = self.number
        super().save(*args, **kwargs)

    class Meta:
        ordering = [
            F('equipment__owner__name').asc(),
            F('equipment__equipment_class__name').asc(),
            F('equipment__fleet_number').asc()
        ]

    def __str__(self) -> str:
        try:
            equipment = f'{self.equipment.__str__()} {self.number.as_international}'
        except ObjectDoesNotExist:
            equipment = f'UNASSIGNED {self.number.as_international}'
        return equipment


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

    def __str__(self) -> str:
        return f'{self.equipment_class.name} - {self.manufacturer.name} {self.name}'


class PlateNumber(Model):
    """
    LTO conduction number of equipment
    """
    plate_number = AlphaNumeric(max_length=10)

    class Meta:
        ordering = [F('plate_number').asc()]

    def __str__(self) -> str:
        return self.plate_number


class ProviderEquipment(Equipment):
    """
    Equipment units of external service providers. The input should only be the
    providers name, equipment type, and the body number of equipment.
    """
    objects = ProviderEquipmentManager()

    def clean(self) -> None:
        if not self.equipment_class:
            raise ValidationError("Equipment class should not be empty.")
        try:
            model = EquipmentModel.objects.get(
                equipment_class__name=self.equipment_class.name,
                manufacturer__name='Unknown',
                name='Unknown'
            )
        except ObjectDoesNotExist:
            manufacturer = EquipmentModel.objects.get(name='Unkown')
            model = EquipmentModel(name='Unkown',
                                   equipment_class=self.equipment_class,
                                   manufacturer=manufacturer)
            model.save()
            model.refresh_from_db()
        self.model = model
        super().clean()

    class Meta:
        proxy = True
        verbose_name_plural = 'provider equipment units'


class ProviderEquipmentRegistry(Model):
    """
    Annual registry of providers' equipment units.
    """
    ACQUISITION_CONDITION = (
        (True, 'Used'),
        (False, 'New')
    )

    acquisition_condition = BooleanField(
        default=True, choices=ACQUISITION_CONDITION
    )
    capacity = ForeignKey(Capacity, blank=True, null=True, on_delete=PROTECT)
    chassis_serial_number = ForeignKey(
        ChassisSerialNumber, blank=True, null=True, on_delete=PROTECT
    )
    delivery_year = PositiveSmallIntegerField()
    engine_serial_number = ForeignKey(
        EngineSerialNumber, blank=True, null=True, on_delete=PROTECT
    )
    equipment = ForeignKey(ProviderEquipment, on_delete=PROTECT)
    model = ForeignKey(EquipmentModel, on_delete=PROTECT)
    plate_number = ForeignKey(
        PlateNumber, blank=True, null=True, on_delete=PROTECT
    )
    pull_out_date = DateField(blank=True, null=True)
    registration_date = DateField()
    safety_inspection_id = PositiveSmallIntegerField()
    sap_registered = BooleanField(default=False)
    warehouse_registered = BooleanField(default=False)
    year = PositiveSmallIntegerField(default=2010)

    # Auto-computed fields used for multiplechoice filters
    x_equipment_class = CharField(max_length=40, blank=True, null=True)
    x_contractor = CharField(max_length=40, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.year = self.registration_date.year
        #TODO: remove this when triggers are created
        self.x_equipment_class = self.equipment.equipment_class.name
        self.x_contractor = self.equipment.owner.name
        # ENDTODO
        super().save(*args, **kwargs)
        latest_registry = self.equipment \
            .providerequipmentregistry_set \
            .order_by('-registration_date') \
            .first()
        self.equipment.date_acquired = datetime(
            latest_registry.delivery_year, 1, 1
        )
        self.equipment.model = self.model
        if self.chassis_serial_number:
            self.equipment.chassis_serial_number = self.chassis_serial_number.name
        if self.engine_serial_number:
            self.equipment.engine_serial_number = self.engine_serial_number.name
        if self.plate_number:
            self.equipment.plate_number = self.plate_number.plate_number
        self.equipment.save()

    class Meta:
        constraints = [
            CheckConstraint(check=Q(delivery_year__gt=2010),
                            name='contractor_registry_min_year'),
            CheckConstraint(check=Q(delivery_year__lt=2050),
                            name='contractor_registry_max_year'),
            UniqueConstraint(
                fields=['safety_inspection_id', 'year'],
                name='unique_safety_inspection_id'
            )
        ]
        ordering = [
            F('year').desc(),
            F('equipment__owner__name').asc(),
            F('equipment__equipment_class__name').asc(),
            F('equipment__fleet_number').asc()
        ]
        verbose_name_plural = 'provider equipment registry'

    def __str__(self) -> str:
        if self.registration_date:
            return f'{self.registration_date.year} - {self.equipment.__str__()}'
        return self.equipment.__str__()


class TrackedExcavator(Model):
    fleet_number = PositiveSmallIntegerField(unique=True)

    class Meta:
        ordering = ['fleet_number']

    def __str__(self):
        return f'TX-{self.fleet_number}'

