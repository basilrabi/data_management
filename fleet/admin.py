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
    pass


@register(EquipmentClass)
class EquipmentClassAdmin(ModelAdmin):
    list_display = ('__str__', 'description')


@register(EquipmentManufacturer)
class EquipmentManufacturerAdmin(ModelAdmin):
    list_display = ('__str__', 'description')


@register(EquipmentModel)
class EquipmentModelAdmin(ModelAdmin):
    pass


@register(TrackedExcavator)
class TrackedExcavatorAdmin(ModelAdmin):
    pass
