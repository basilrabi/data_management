from django.contrib.admin import ModelAdmin, register

from .models.equipment import (
    Equipment,
    EquipmentClass,
    EquipmentManufacturer,
    EquipmentModel,
    TrackedExcavator
)


@register(Equipment)
class EquipmentAdmin(ModelAdmin):
    autocomplete_fields = ['model']
    exclude = ('equipment_class',)
    list_display = ('__str__', 'model', 'engine_serial_number')
    list_filter = ['owner', 'equipment_class']
    search_fields = ['fleet_number',
                     'model__manufacturer__name',
                     'model__name',
                     'engine_serial_number',]


@register(EquipmentClass)
class EquipmentClassAdmin(ModelAdmin):
    list_display = ('name', 'description')


@register(EquipmentManufacturer)
class EquipmentManufacturerAdmin(ModelAdmin):
    list_display = ('__str__', 'description')


@register(EquipmentModel)
class EquipmentModelAdmin(ModelAdmin):
    list_display = ('equipment_class', 'manufacturer', 'name')
    search_fields = ['equipment_class__name', 'manufacturer__name', 'name']


@register(TrackedExcavator)
class TrackedExcavatorAdmin(ModelAdmin):
    pass
