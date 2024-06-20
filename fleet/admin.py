from django.contrib.admin import ModelAdmin, TabularInline, register
from django.db.models import TextField
from django.forms import Textarea

from custom.admin import ReadOnlyAdmin
from organization.admin import ServiceProviderAdmin
from organization.models import Organization, ServiceProvider
from .filters import (
    ProviderEquipmentRegistryClassFilter,
    ProviderEquipmentRegistryProviderFilter
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
    PlateNumber,
    ProviderEquipment,
    ProviderEquipmentRegistry,
    ProviderEquipmentRequirement,
    ProviderEquipmentRequirementDetail,
    TrackedExcavator
)


class AdditionalEquipmentCostInline(TabularInline):
    extra = 0
    fields = ('description',
              'acquisition_cost',
              'date_acquired',
              'asset_code',
              'service_life')
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


@register(Capacity)
class CapacityAdmin(ModelAdmin):
    list_display = ('__str__', 'value', 'unit_of_measure')
    list_editable = ('unit_of_measure', 'value')
    search_fields = ['unit_of_measure__description',
                     'unit_of_measure__name',
                     'value']


@register(ChassisSerialNumber)
class SerialNumberAdmin(ModelAdmin):
    search_fields = ['name']


@register(EngineSerialNumber)
class EngineSerialNumberAdmin(ModelAdmin):
    search_fields = ['name']


@register(Equipment)
class EquipmentAdmin(ModelAdmin):

    autocomplete_fields = ['model']
    exclude = ('equipment_class',)
    inlines = [AdditionalEquipmentCostInline]
    list_display = ('__str__', 'model', 'plate_number', 'fleet_number','department_assigned')
    list_filter = ['owner', 'active', 'equipment_class']
    search_fields = ['engine_serial_number',
                     'fleet_number',
                     'model__manufacturer__name',
                     'model__name',]

    fields_1 = ('fleet_number',
                'owner',
                'department_assigned',
                'model',
                'year_model',
                'certificate_of_registration_no',
                'cr_date',
                'mv_file_no',
                'acquisition_cost',
                'date_acquired')

    fields_2 = ('asset_tag_id',
                'asset_serial_number',
                'asset_code',
                'service_life',
                'engine_serial_number',
                'plate_number',
                'body_type',
                'month_of_registration',
                'chassis_serial_number',
                'description',
                'active')

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


@register(PlateNumber)
class PlateNumberAdmin(ModelAdmin):
    search_fields = ['plate_number']


@register(ProviderEquipment)
class ProviderEquipmentAdmin(ModelAdmin):
    autocomplete_fields = ['owner']
    fields = ['owner', 'equipment_class', 'fleet_number']
    search_fields = ['equipment_class__name',
                     'fleet_number',
                     'owner__name']


@register(ProviderEquipmentRegistry)
class ProviderEquipmentRegistryAdmin(ModelAdmin):
    autocomplete_fields = ['capacity',
                           'chassis_serial_number',
                           'engine_serial_number',
                           'equipment',
                           'model',
                           'plate_number']
    date_hierarchy = 'registration_date'
    fields = ['registration_date',
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
              'omt_registered']
    list_display = ['__str__'] + fields
    list_editable = fields
    list_filter = [
        'sap_registered',
        'warehouse_registered',
        'omt_registered',
        ProviderEquipmentRegistryClassFilter,
        ProviderEquipmentRegistryProviderFilter
    ]
    search_fields = ['chassis_serial_number__name',
                     'engine_serial_number__name',
                     'plate_number__plate_number',
                     'safety_inspection_id']


@register(ProviderEquipmentRequirement)
class ProviderEquipmentRequirementAdmin(ModelAdmin):
    autocomplete_fields = ['contractor']
    inlines = [ProviderEquipmentRequirementDetailInline]
    list_filter = ['contractor', 'year']


@register(TrackedExcavator)
class TrackedExcavatorAdmin(ModelAdmin):
    pass

