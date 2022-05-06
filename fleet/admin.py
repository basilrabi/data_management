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
    exclude = ('equipment_class',)
    list_display = ('__str__', 'model', 'serial_number')
    list_filter = ['owner', 'equipment_class']
    search_fields = ['fleet_number',
                     'model__manufacturer__name',
                     'model__name',
                     'serial_number',]


@register(EquipmentClass)
class EquipmentClassAdmin(ModelAdmin):
    list_display = ('name', 'description')


@register(EquipmentManufacturer)
class EquipmentManufacturerAdmin(ModelAdmin):
    list_display = ('__str__', 'description')


@register(EquipmentModel)
class EquipmentModelAdmin(ModelAdmin):
    pass


@register(TrackedExcavator)
class TrackedExcavatorAdmin(ModelAdmin):
    pass
