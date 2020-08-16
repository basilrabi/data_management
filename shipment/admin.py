from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import (
    DateField, ExpressionWrapper, F, IntegerField, TextField
)
from django.forms import Textarea
from django.forms.models import BaseInlineFormSet
from django.db.models.functions import Cast

from custom.functions import Round, print_tz_manila
from .models.lct import LCT, LCTContract, Trip, TripDetail
from .models.dso import (
    ApprovedLayDaysStatement,
    Buyer,
    Destination,
    LayDaysDetail,
    LayDaysStatement,
    Product,
    Shipment,
    Vessel
)
from .models.proxy import FinalShipmentDetail

# pylint: disable=no-member


class IntervalFromInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return

        end_stamp = None
        timestamps = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            timestamp = form.cleaned_data.get('interval_from')
            if timestamp in timestamps:
                raise ValidationError(f'{str(print_tz_manila(timestamp))} is duplicated.')
            if form.cleaned_data.get('interval_class') == 'end':
                if not end_stamp:
                    end_stamp = timestamp
                else:
                    raise ValidationError('Only one end is allowed.')
            timestamps.append(timestamp)
        if end_stamp:
            if end_stamp < max(timestamps):
                raise ValidationError(f'End ({str(print_tz_manila(end_stamp))}) should have the last time stamp.')


class LayDaysDetailInline(admin.TabularInline):
    model = LayDaysDetail
    extra = 0
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={'rows':1, 'cols':40})}
    }
    formset = IntervalFromInlineFormSet


class LCTContractInline(admin.TabularInline):
    model = LCTContract
    extra = 0


class TripDetailInline(admin.TabularInline):
    model = TripDetail
    extra = 0
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={'rows':1, 'cols':40})}
    }
    formset = IntervalFromInlineFormSet


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(FinalShipmentDetail)
class FinalShipmentDetailAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Boulders', {
            'fields': (
                'boulders_tonnage',
                'boulders_processing_cost',
                'boulders_freight_cost'
            )
        }),
        ('Final Specification', {
            'fields': (
                'buyer',
                'base_price',
                'final_price',
                'final_ni',
                'final_fe',
                'final_moisture',
                'remarks'
            )
        })
    )
    list_display = (
        'name',
        'vessel',
        'final_ni',
        'final_fe',
        'final_price',
        'final_moisture',
        'diff_ni',
        'diff_wmt',
        'demurrage',
        'despatch'
    )
    search_fields = ['name', 'vessel__name']

    def get_queryset(self, request):
        qs = super().get_queryset(request) \
            .annotate(
                diff_ni=F('shipmentloadingassay__ni') - F('shipmentdischargeassay__ni'),
                diff_wmt=ExpressionWrapper(
                    F('laydaysstatement__tonnage') - F('shipmentdischargeassay__wmt'),
                    output_field=IntegerField()
                )
            )
        return qs

    def diff_ni(self, obj):
        return obj.diff_ni

    def diff_wmt(self, obj):
        return obj.diff_wmt

    diff_ni.short_description = 'Δ%Ni'
    diff_wmt.short_description = 'ΔWMT'


@admin.register(LayDaysStatement)
class LayDaysStatementAdmin(admin.ModelAdmin):
    autocomplete_fields = ['shipment']
    date_hierarchy = 'laydaysdetail__interval_from'
    inlines = [LayDaysDetailInline]
    list_display = (
        '__str__',
        'vessel',
        'commenced_laytime',
        'completed_loading',
        'demurrage',
        'despatch',
        'PDF',
        'csv',
        'approved'
    )
    readonly_fields = [
        'date_saved',
        'date_computed',
        'commenced_laytime',
        'commenced_loading',
        'completed_loading',
        'time_allowed',
        'additional_laytime',
        'demurrage',
        'despatch'
    ]
    search_fields = ['shipment__name']

    def get_queryset(self, request):
        qs = super().get_queryset(request).annotate(
            approved=F('approvedlaydaysstatement__approved')
        )
        return qs

    def approved(self, obj):
        return obj.approved

    approved.admin_order_field = 'approved'
    approved.boolean = True


@admin.register(ApprovedLayDaysStatement)
class ApprovedLayDaysStatementAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'approved', 'PDF', 'csv')
    search_fields = ['statement__shipment__name']


@admin.register(LCT)
class LCTAdmin(admin.ModelAdmin):
    inlines = [LCTContractInline]
    list_display = ('name', 'capacity')
    list_filter = ['capacity']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    autocomplete_fields = ['vessel']
    date_hierarchy = 'laydaysstatement__laydaysdetail__interval_from'
    fieldsets = (
        (None, {'fields': (
            'name',
            'product',
            'vessel',
            'destination',
            'target_tonnage',
            'dump_truck_trips'
        )}),
        ('Laytime', {'fields': ('demurrage','despatch',)}),
        ('Sales Contract', {
            'classes': ('collapse',),
            'fields': (
                'buyer',
                'base_price',
                'spec_tonnage',
                'spec_ni',
                'spec_fe',
                'spec_moisture'
            )
        })
    )
    list_display = (
        'name',
        'vessel',
        'dump_truck_trips',
        'tonnage',
        'ni',
        'fe',
        'moisture',
        'demurrage',
        'despatch',
        'completion',
        'number'
    )
    search_fields = ['name', 'vessel__name']

    def get_queryset(self, request):
        qs = super().get_queryset(request) \
            .annotate(
                tonnage=F('laydaysstatement__tonnage'),
                ni=Round(F('shipmentloadingassay__ni'), 2),
                fe=Round(F('shipmentloadingassay__fe'), 2),
                moisture=Round(F('shipmentloadingassay__moisture'), 2),
                completion=Cast(F('laydaysstatement__completed_loading'), DateField())
            )
        return qs

    def completion(self, obj):
        return obj.completion

    def fe(self, obj):
        return obj.fe

    def moisture(self, obj):
        return obj.moisture

    def ni(self, obj):
        return obj.ni

    def tonnage(self, obj):
        return obj.tonnage

    fe.short_description = '%Fe'
    moisture.short_description = '%H₂O'
    ni.short_description = '%Ni'


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    autocomplete_fields = ['lct', 'vessel']
    inlines = [TripDetailInline]
    list_display = (
        'lct',
        'interval_from',
        'interval_to',
        'vessel',
        'dump_truck_trips',
        'cycle',
        'valid',
        'continuous'
    )
    list_filter = ['continuous', 'status', 'valid']
    readonly_fields = ['valid', 'continuous', 'interval_from', 'interval_to']
    search_fields = ['lct__name', 'vessel__name']


@admin.register(Vessel)
class VesselAdmin(admin.ModelAdmin):
    exclude = ('stripped_name',)
    list_display = ('__str__',)
    search_fields = ['name']
