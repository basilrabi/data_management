from django.contrib.admin import ModelAdmin, TabularInline, register
from django.db.models import TextField
from django.forms import Textarea
from django.utils import timezone
from nested_admin import NestedModelAdmin, NestedTabularInline

from custom.admin import ReadOnlyAdmin
from organization.admin import ServiceProviderAdmin
from organization.models import Organization, ServiceProvider
from .filters import (
    EquipmentBreakdownClassFilter,
    ProviderEquipmentRegistryClassFilter,
    ProviderEquipmentRegistryProviderFilter
)
from .forms import (
    EquipmentAdminForm,
    InhouseEquipmentAdminForm,
    ProviderEquipmentRegistryAdminForm
)
from .models.equipment import (
    AdditionalEquipmentCost,
    BodyType,
    Capacity,
    ChassisSerialNumber,
    EngineSerialNumber,
    Equipment,
    EquipmentClass,
    EquipmentIdlingTime,
    EquipmentIgnitionStatus,
    EquipmentManufacturer,
    EquipmentMobileNumber,
    EquipmentModel,
    InhouseEquipment,
    PlateNumber,
    ProviderEquipment,
    ProviderEquipmentRegistry,
    ProviderEquipmentRequirement,
    ProviderEquipmentRequirementDetail,
    TrackedExcavator
)
from .models.maintenance import (
    BreakdownStatus,
    CauseCode,
    ComponentCode,
    DamageCode,
    EquipmentBreakdown,
    MaintenanceOperation,
    MaintenanceTask,
    MaintenanceTaskManpower,
    PartGroup,
    WorkCenter
)
from .models.proxy import EquipmentBreakdownReport


class MaintenanceTaskManpowerInline(NestedTabularInline):
    autocomplete_fields = ['work_center']
    extra = 0
    model = MaintenanceTaskManpower


class MaintenanceTaskInline(NestedTabularInline):
    extra = 0
    inlines = [MaintenanceTaskManpowerInline]
    model = MaintenanceTask


class MaintenanceOperationInline(NestedTabularInline):
    autocomplete_fields = [
        'cause',
        'component',
        'damage',
        'part_group'
    ]
    extra = 0
    inlines = [MaintenanceTaskInline]
    model = MaintenanceOperation


class AdditionalEquipmentCostInline(TabularInline):
    extra = 0
    fields = (
        'description',
        'acquisition_cost',
        'date_acquired',
        'asset_code',
        'service_life'
    )
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 40})}
    }
    model = AdditionalEquipmentCost


class ProviderEquipmentRequirementDetailInline(TabularInline):
    autocomplete_fields = ['equipment']
    extra = 0
    model = ProviderEquipmentRequirementDetail


@register(BodyType)
class BodyTypeAdmin(ModelAdmin):
    list_display = ('name', 'description')


@register(BreakdownStatus)
class BreakdownStatusAdmin(ModelAdmin):
    search_fields = ['name']


@register(Capacity)
class CapacityAdmin(ModelAdmin):
    list_display = ('__str__', 'value', 'unit_of_measure')
    list_editable = ('unit_of_measure', 'value')
    search_fields = [
        'unit_of_measure__description',
        'unit_of_measure__name',
        'value'
    ]


@register(CauseCode)
class CauseCodeAdmin(ModelAdmin):
    search_fields = ['name']


@register(ChassisSerialNumber)
class SerialNumberAdmin(ModelAdmin):
    search_fields = ['name']


@register(ComponentCode)
class ComponentCodeAdmin(ModelAdmin):
    search_fields = ['name']


@register(DamageCode)
class DamageCodeAdmin(ModelAdmin):
    search_fields = ['name']


@register(EngineSerialNumber)
class EngineSerialNumberAdmin(ModelAdmin):
    search_fields = ['name']


@register(Equipment)
class EquipmentAdmin(ModelAdmin):
    autocomplete_fields = ['model']
    exclude = ('equipment_class',)
    form = EquipmentAdminForm
    inlines = [AdditionalEquipmentCostInline]
    list_display = ('__str__', 'model', 'plate_number', 'fleet_number','department_assigned')
    list_filter = ['owner', 'active', 'equipment_class']
    search_fields = [
        'engine_serial_number',
        'equipment_class__name',
        'fleet_number',
        'model__manufacturer__name',
        'model__name',
        'owner__name'
    ]

    fields_1 = (
        'fleet_number',
        'owner',
        'department_assigned',
        'model',
        'year_model',
        'certificate_of_registration_no',
        'cr_date',
        'mv_file_no',
        'acquisition_cost',
        'date_acquired'
    )

    fields_2 = (
        'asset_tag_id',
        'asset_serial_number',
        'asset_code',
        'service_life',
        'engine_serial_number',
        'plate_number',
        'body_type',
        'month_of_registration',
        'chassis_serial_number',
        'description',
        'active'
    )

    def add_view(self, request, form_url='', extra_context=None):

        if request.user.groups.all().filter(name='camp admin').exists():
            if_camp = 'date_disposal'
        elif request.user.is_superuser:
            if_camp = ('date_phased_out', 'date_disposal')
        else:
            if_camp = 'date_phased_out'

        self.fields = self.fields_1 + (if_camp,) + self.fields_2
        return super().add_view(request, form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):

        if request.user.groups.all().filter(name='camp admin').exists():
            if_camp = 'date_disposal'
        elif request.user.is_superuser:
            if_camp = ('date_phased_out', 'date_disposal')
        else:
            if_camp = 'date_phased_out'

        self.fields = self.fields_1 + (if_camp,) + self.fields_2
        return super().change_view(request, object_id, form_url, extra_context=extra_context)


@register(EquipmentBreakdown)
class EquipmentBreakdownAdmin(NestedModelAdmin):
    inlines = [MaintenanceOperationInline]
    list_display = (
        'equipment',
        'status',
        'breakdown_duration'
    )
    list_filter = (EquipmentBreakdownClassFilter,)
    readonly_fields = ('equipment',)

    def breakdown_duration(self, obj):
        return timezone.now() - obj.reported_on


@register(EquipmentBreakdownReport)
class EquipmentBreakdownReportAdmin(ModelAdmin):
    autocomplete_fields = ['equipment']
    fields = (
        'equipment',
        'description',
        'reported_on',
        'reporter',
        'status'
    )
    list_display = (
        'equipment',
        'reported_on',
        'status'
    )
    list_filter = (EquipmentBreakdownClassFilter,)
    readonly_fields = (
        'reported_on',
        'reporter',
        'status'
    )

    def save_form(self, request, form, change):
        obj = super().save_form(request, form, change)
        if not change:
            obj.reporter = request.user
        return obj


@register(EquipmentClass)
class EquipmentClassAdmin(ModelAdmin):
    list_display = ('name', 'description', 'code')
    search_fields = ('name',)


@register(EquipmentIdlingTime)
class EquipmentIdlingTimeAdmin(ReadOnlyAdmin):
    date_hierarchy = 'time_stamp'
    list_display = ('equipment', 'time_stamp', 'idling')


@register(EquipmentIgnitionStatus)
class EquipmentIgnitionStatusAdmin(ReadOnlyAdmin):
    date_hierarchy = 'time_stamp'
    list_display = ('equipment', 'time_stamp', 'ignition')


@register(EquipmentManufacturer)
class EquipmentManufacturerAdmin(ModelAdmin):
    list_display = ('__str__', 'description')


@register(EquipmentMobileNumber)
class EquipmentMobileNumberAdmin(ModelAdmin):
    fields = ('equipment', 'number')
    list_display = ('equipment', 'number')
    search_fields = (
        'equipment__equipment_class__name',
        'equipment__fleet_number',
        'equipment__owner__name'
    )


@register(EquipmentModel)
class EquipmentModelAdmin(ModelAdmin):
    list_display = ('equipment_class', 'manufacturer', 'name')
    search_fields = ['equipment_class__name', 'manufacturer__name', 'name']


@register(InhouseEquipment)
class InhouseEquipmentAdmin(ModelAdmin):
    autocomplete_fields = ['model']
    exclude = ('equipment_class',)
    form = InhouseEquipmentAdminForm
    inlines = [AdditionalEquipmentCostInline]
    list_display = ('__str__', 'model', 'plate_number', 'fleet_number','department_assigned')
    list_filter = ['active', 'equipment_class']
    search_fields = [
        'engine_serial_number',
        'equipment_class__name',
        'fleet_number',
        'model__manufacturer__name',
        'model__name',
    ]

    fields_1 = (
        'fleet_number',
        'department_assigned',
        'model',
        'year_model',
        'certificate_of_registration_no',
        'cr_date',
        'mv_file_no',
        'acquisition_cost',
        'date_acquired'
    )

    fields_2 = (
        'asset_tag_id',
        'asset_serial_number',
        'asset_code',
        'service_life',
        'engine_serial_number',
        'plate_number',
        'body_type',
        'month_of_registration',
        'chassis_serial_number',
        'description',
        'active'
    )

    def add_view(self, request, form_url='', extra_context=None):

        if request.user.groups.all().filter(name='camp admin').exists():
            if_camp = 'date_disposal'
        elif request.user.is_superuser:
            if_camp = ('date_phased_out', 'date_disposal')
        else:
            if_camp = 'date_phased_out'

        self.fields = self.fields_1 + (if_camp,) + self.fields_2
        return super().add_view(request, form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):

        if request.user.groups.all().filter(name='camp admin').exists():
            if_camp = 'date_disposal'
        elif request.user.is_superuser:
            if_camp = ('date_phased_out', 'date_disposal')
        else:
            if_camp = 'date_phased_out'

        self.fields = self.fields_1 + (if_camp,) + self.fields_2
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def save_form(self, request, form, change):
        obj = super().save_form(request, form, change)
        obj.owner = Organization.objects.get(name='TMC')
        return obj


@register(PartGroup)
class PartGroupAdmin(ModelAdmin):
    search_fields = ['name']


@register(PlateNumber)
class PlateNumberAdmin(ModelAdmin):
    search_fields = ['plate_number']


@register(ProviderEquipment)
class ProviderEquipmentAdmin(ModelAdmin):
    autocomplete_fields = ['owner']
    fields = ['owner', 'equipment_class', 'fleet_number']
    search_fields = [
        'equipment_class__name',
        'fleet_number',
        'owner__name'
    ]


@register(ProviderEquipmentRegistry)
class ProviderEquipmentRegistryAdmin(ModelAdmin):
    autocomplete_fields = [
        'capacity',
        'chassis_serial_number',
        'engine_serial_number',
        'equipment',
        'model',
        'plate_number'
    ]
    date_hierarchy = 'registration_date'
    fields = [
        'registration_date',
        'equipment',
        'safety_inspection_id',
        'model',
        'engine_serial_number',
        'chassis_serial_number',
        'plate_number',
        'delivery_year',
        'acquisition_condition',
        'capacity',
        'pull_out_date',
        'sap_registered',
        'warehouse_registered',
        'omt_registered'
    ]
    form = ProviderEquipmentRegistryAdminForm
    list_display = ['__str__'] + fields
    list_editable = fields
    list_filter = [
        'sap_registered',
        'warehouse_registered',
        'omt_registered',
        ProviderEquipmentRegistryClassFilter,
        ProviderEquipmentRegistryProviderFilter
    ]
    search_fields = [
        'chassis_serial_number__name',
        'engine_serial_number__name',
        'equipment__equipment_class__name',
        'equipment__fleet_number',
        'equipment__owner__name',
        'plate_number__plate_number',
        'safety_inspection_id'
    ]


@register(ProviderEquipmentRequirement)
class ProviderEquipmentRequirementAdmin(ModelAdmin):
    autocomplete_fields = ['contractor']
    inlines = [ProviderEquipmentRequirementDetailInline]
    list_filter = ['contractor', 'year']


@register(TrackedExcavator)
class TrackedExcavatorAdmin(ModelAdmin):
    pass


@register(WorkCenter)
class WorkCenterAdmin(ModelAdmin):
    search_fields = ['name']

