from django.contrib import admin
from django.db.models import F

from custom.admin_gis import TMCLocationAdmin
from custom.models import User
from personnel.models.person import Person

from .models.piling import PilingMethod, TripsPerPile
from .models.proxy import (
    AcquiredMiningSample,
    ChinaShipmentAssay,
    MiningSampleAssay,
    PamcoShipmentAssay
)
from .models.sample import (
    ApprovedShipmentLoadingAssay,
    MiningSample,
    MiningSampleIncrement,
    MiningSampleReport,
    Laboratory,
    Lithology,
    ShipmentDischargeLotAssay,
    ShipmentLoadingAssay,
    ShipmentLoadingLotAssay
)

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


class ShipmentDischargeLotAssayInline(admin.TabularInline):
    model = ShipmentDischargeLotAssay
    extra = 0
    fields = ('lot', 'wmt', 'moisture', 'ni')


class ShipmentLoadingLotAssayInline(ShipmentDischargeLotAssayInline):
    model = ShipmentLoadingLotAssay


class TripsPerPileInline(admin.TabularInline):
    model = TripsPerPile
    extra = 0


@admin.register(Laboratory)
class LaboratoryAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(AcquiredMiningSample)
class AcquiredMiningSampleAdmin(admin.ModelAdmin):
    list_display = ('__str__',
                    'dumping_area',
                    'trips',
                    'ready_for_delivery')
    exclude = ('ridge',
               'start_collection',
               'end_collection',
               'trips',
               'ready_for_delivery')


@admin.register(ChinaShipmentAssay)
class ChinaShipmentAssayAdmin(admin.ModelAdmin):
    autocomplete_fields = ['shipment']
    fields = (
        'shipment', 'laboratory', 'wmt', 'dmt', 'moisture',
        'ni', 'fe', 'sio2', 'al2o3', 'mgo', 'p', 's', 'cao'
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request).exclude(laboratory__name='PAMCO')
        return qs


@admin.register(Lithology)
class LithologyAdmin(admin.ModelAdmin):
    pass


@admin.register(MiningSampleAssay)
class MiningSampleAssayAdmin(admin.ModelAdmin):
    list_display = ('__str__',
                    'date_received_for_preparation',
                    'date_prepared',
                    'date_received_for_analysis',
                    'date_analyzed')


@admin.register(MiningSampleReport)
class MiningSampleReportAdmin(admin.ModelAdmin):
    list_display = ('date',
                    'shift_collected',
                    'piling_method',
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


@admin.register(PamcoShipmentAssay)
class PamcoShipmentAssayAdmin(admin.ModelAdmin):
    autocomplete_fields = ['shipment']
    fields = (
        'shipment', 'wmt', 'dmt', 'moisture', 'ni', 'ni_ton', 'co', 'cr', 'mn',
        'fe', 'sio2', 'cao', 'mgo', 'al2o3', 'p', 's', 'ignition_loss'
    )
    inlines = [ShipmentDischargeLotAssayInline]
    readonly_fields = ('wmt', 'dmt', 'moisture', 'ni', 'ni_ton')

    def get_queryset(self, request):
        qs = super().get_queryset(request).filter(laboratory__name='PAMCO')
        return qs


@admin.register(ShipmentLoadingAssay)
class ShipmentLoadingAssayAdmin(admin.ModelAdmin):
    autocomplete_fields = ['shipment']
    fields = (
        'date', 'shipment', 'chemist', 'wmt', 'dmt', 'moisture', 'ni', 'ni_ton',
        'fe', 'mgo', 'sio2', 'cr', 'co'
    )
    inlines = [ShipmentLoadingLotAssayInline]
    list_display = ('__str__', 'approved', 'PDF')
    readonly_fields = ('wmt', 'dmt', 'moisture', 'ni', 'ni_ton')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'chemist':
            kwargs["queryset"] = User.objects.filter(groups__name='chemist')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request) \
            .annotate(approved=F('approvedshipmentloadingassay__approved'))
        return qs

    def approved(self, obj):
        return obj.approved

    approved.admin_order_field = 'approved'
    approved.boolean = True


@admin.register(ApprovedShipmentLoadingAssay)
class ApprovedShipmentLoadingAssayAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'approved', 'PDF')
