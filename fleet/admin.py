from django.contrib.admin import ModelAdmin, TabularInline, register
from django.db.models import TextField
from django.forms import Textarea

from custom.admin import ReadOnlyAdmin
from organization.admin import ServiceProviderAdmin
from organization.models import Organization, ServiceProvider
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
    EquipmentModel,
    PlateNumber,
    ProviderEquipment,
    ProviderEquipmentRegistry,
    TrackedExcavator
)


class AdditionalEquipmentCostInline(TabularInline):
    model = AdditionalEquipmentCost
    extra = 0
    fields = ('description',
              'acquisition_cost',
              'date_acquired',
              'asset_code',
              'service_life')
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={'rows':1, 'cols':40})}
    }


@register(BodyType)
class BodyTypeAdmin(ModelAdmin):
    list_display = ('name', 'description')


@register(Capacity)
class CapacityAdmin(ModelAdmin):
    list_display = ('__str__', 'value', 'unit_of_measure')
    list_editable = ('unit_of_measure', 'value')
    search_fields = ['value', 'unit_of_measure']


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
    list_display = ('name', 'description')


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
    search_fields = ['chassis_serial_number__name',
                     'engine_serial_number__name',
                     'fleet_number',
                     'model__manufacturer__name',
                     'model__name',
                     'owner__name']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'owner':
            # TODO: This is a stub. The goal is to filter the Organization in
            # the auto-complete field to only contractors. This should more
            # realistic to implement in java script by capturing the GET
            # Request and filter the query set in the searchable foreign key.
            # kwargs['queryset'] = ServiceProvider.objects.filter(service='Contractor')
            pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(owner__service='Contractor')


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
              'warehouse_registered']
    list_display = ['__str__'] + fields
    list_editable = fields


@register(TrackedExcavator)
class TrackedExcavatorAdmin(ModelAdmin):
    pass

