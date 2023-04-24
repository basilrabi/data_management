from django.contrib.admin import ModelAdmin, register

from .models.equipment import (
    BodyType,
    Equipment,
    EquipmentClass,
    EquipmentManufacturer,
    EquipmentModel,
    TrackedExcavator
)


@register(BodyType)
class BodyTypeAdmin(ModelAdmin):
    list_display = ('name', 'description')


@register(Equipment)
class EquipmentAdmin(ModelAdmin):

    autocomplete_fields = ['model']
    exclude = ('equipment_class',)
    list_display = ('__str__', 'model', 'plate_number', 'engine_serial_number')
    list_filter = ['owner', 'equipment_class']
    search_fields = ['fleet_number',
                     'model__manufacturer__name',
                     'model__name',
                     'engine_serial_number',]

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
