from django.contrib import admin

from custom.admin_gis import TMCLocationAdmin
from personnel.models.person import Person

from .models.piling import PilingMethod, TripsPerPile
from .models.sample import (Material,
                            MiningSample,
                            MiningSampleAssay,
                            MiningSampleIncrement,
                            MiningSampleReport)

# pylint: disable=no-member

class MiningSampleIncrementInline(admin.TabularInline):
    model = MiningSampleIncrement
    extra = 0

    this_obj = None
    def get_formset(self, request, obj=None, **kwargs):
        if obj:
            self.this_obj = obj
        return super().get_formset(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'sample':
            kwargs["queryset"] = MiningSample.objects \
                .filter(ready_for_delivery=False)
            if self.this_obj:
                for inc in self.this_obj.miningsampleincrement_set.all():
                    kwargs["queryset"] |= MiningSample.objects \
                        .filter(id=inc.sample.id) \
                        .exclude(ready_for_delivery=False)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class TripsPerPileInline(admin.TabularInline):
    model = TripsPerPile
    extra = 0

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    pass

@admin.register(MiningSample)
class MiningSampleAdmin(admin.ModelAdmin):
    list_display = ('__str__',
                    'dumping_area',
                    'trips',
                    'ready_for_delivery',
                    'harvested',
                    'year'
    )
    exclude = ('ridge',
               'start_collection',
               'year',
               'end_collection',
               'trips',
               'ready_for_delivery')

@admin.register(MiningSampleAssay)
class MiningSampleAssayAdmin(admin.ModelAdmin):
    list_display = ('__str__',
                    'date_received_for_preparation',
                    'date_prepared',
                    'date_received_for_analysis',
                    'date_analyzed')

@admin.register(MiningSampleReport)
class MiningSampleReportAdmin(TMCLocationAdmin):
    list_display = ('date',
                    'shift_collected',
                    'piling_method',
                    'material',
                    'dumping_area')

    def add_view(self, request, form_url='', extra_context=None):
        self.exclude = ('sampler', 'supervisor', 'foreman')
        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = [MiningSampleIncrementInline]
        self.exclude = None
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'supervisor':
            kwargs["queryset"] = Person.objects.distinct().filter(
                employmentrecord__designation__name__contains='SUPERVISOR'
            )
        if db_field.name == 'foreman':
            kwargs["queryset"] = Person.objects.distinct().filter(
                employmentrecord__designation__name__contains='FOREMAN'
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'sampler':
            kwargs["queryset"] = Person.objects.distinct().filter(
                employmentrecord__designation__name__contains='SAMPLER'
            )
        return super().formfield_for_manytomany(db_field, request, **kwargs)

@admin.register(PilingMethod)
class PilingMethodAdmin(admin.ModelAdmin):
    inlines = [TripsPerPileInline]
    list_display = ('name', 'present_required_trip')
