from django.contrib.admin import ModelAdmin, TabularInline, register
from django.core.exceptions import ValidationError
from django.db.models import (
    Case,
    ExpressionWrapper,
    F,
    IntegerField,
    TextField,
    When
)
from django.forms import Textarea
from django.forms.models import BaseInlineFormSet
from import_export.admin import ExportMixin
from import_export.fields import Field
from import_export.resources import ModelResource

from custom.functions import Round, print_tz_manila
from location.models.shipment import Anchorage
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


class ShipmentResource(ModelResource):
    number = Field(attribute='number', column_name='Number')
    shipment = Field(attribute='name', column_name='Shipment')
    completion = Field(column_name='Completion')
    buyer_name = Field(attribute='buyer__name', column_name='Buyer')
    destination_name = Field(attribute='destination__name', column_name='Destination')
    product_name = Field(attribute='product__name', column_name='Product')
    vessel_name = Field(attribute='vessel__name', column_name='Vessel')
    loading_ni = Field(attribute='shipmentloadingassay__ni', column_name='Loading %Ni')
    loading_fe = Field(attribute='shipmentloadingassay__fe', column_name='Loading %Fe')
    loading_wmt = Field(attribute='laydaysstatement__tonnage', column_name='Loading WMT')
    loading_dmt = Field(attribute='shipmentloadingassay__dmt', column_name='Loading DMT')
    discharge_lab = Field(attribute='shipmentdischargeassay__laboratory__name', column_name='Discharge Lab')
    discharge_ni = Field(attribute='shipmentdischargeassay__ni', column_name='Discharge %Ni')
    discharge_fe = Field(attribute='shipmentdischargeassay__fe', column_name='Discharge %Fe')
    discharge_wmt = Field(attribute='shipmentdischargeassay__wmt', column_name='Discharge WMT')
    discharge_dmt = Field(attribute='shipmentdischargeassay__dmt', column_name='Discharge DMT')

    class Meta:
        model = FinalShipmentDetail
        exclude = (
            'buyer',
            'destination',
            'id',
            'name',
            'product',
            'vessel'
        )

    def dehydrate_completion(self, shipment):
        if shipment.laydaysstatement.laydaysdetail_set.count() > 0:
            return print_tz_manila(shipment.laydaysstatement.laydaysdetail_set.last().interval_from)


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


class AnchorageInline(TabularInline):
    model = Anchorage
    extra = 0
    exclude = ('geom',)


class LayDaysDetailInline(TabularInline):
    model = LayDaysDetail
    extra = 0
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={'rows':1, 'cols':40})}
    }
    formset = IntervalFromInlineFormSet


class LCTContractInline(TabularInline):
    model = LCTContract
    extra = 0


class TripDetailInline(TabularInline):
    model = TripDetail
    extra = 0
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={'rows':1, 'cols':40})}
    }
    formset = IntervalFromInlineFormSet


@register(Buyer)
class BuyerAdmin(ModelAdmin):
    search_fields = ['name']


@register(Destination)
class DestinationAdmin(ModelAdmin):
    search_fields = ['name']


@register(FinalShipmentDetail)
class FinalShipmentDetailAdmin(ExportMixin, ModelAdmin):
    date_hierarchy = 'laydaysstatement__laydaysdetail__interval_from'
    fieldsets = (
        ('Boulders', {
            'fields': (
                'boulders_tonnage',
                'boulders_processing_cost',
                'boulders_freight_cost',
                'dead_freight'
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
        'object_name',
        'number',
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
    resource_class = ShipmentResource
    search_fields = ['name', 'vessel__name']

    def get_queryset(self, request):
        qs = super().get_queryset(request) \
            .annotate(
                diff_ni=F('shipmentloadingassay__ni') - F('shipmentdischargeassay__ni'),
                diff_wmt=ExpressionWrapper(
                    F('laydaysstatement__tonnage') - F('shipmentdischargeassay__wmt'),
                    output_field=IntegerField()
                ),
                number=F('shipmentnumber__number')
            )
        return qs

    def diff_ni(self, obj):
        return obj.diff_ni

    def diff_wmt(self, obj):
        return obj.diff_wmt

    def number(self, obj):
        return obj.number

    def object_name(self, obj):
        return Shipment.objects.get(id=obj.id).name_html()

    diff_ni.short_description = 'Δ%Ni'
    diff_wmt.short_description = 'ΔWMT'
    object_name.short_description = 'Shipment'


@register(LayDaysStatement)
class LayDaysStatementAdmin(ModelAdmin):
    autocomplete_fields = ['shipment']
    date_hierarchy = 'laydaysdetail__interval_from'
    inlines = [AnchorageInline, LayDaysDetailInline]
    list_display = (
        'object_name',
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

    def object_name(self, obj):
        return LayDaysStatement.objects.get(id=obj.id).shipment.name_html()

    approved.admin_order_field = 'approved'
    approved.boolean = True
    object_name.short_description = 'Shipment'


@register(ApprovedLayDaysStatement)
class ApprovedLayDaysStatementAdmin(ModelAdmin):
    list_display = ('object_name', 'approved', 'PDF', 'csv')
    search_fields = ['statement__shipment__name']

    def object_name(self, obj):
        return ApprovedLayDaysStatement.objects.get(id=obj.id).statement.shipment.name_html()

    object_name.short_description = 'Shipment'


@register(LCT)
class LCTAdmin(ModelAdmin):
    inlines = [LCTContractInline]
    list_display = ('name', 'capacity')
    list_filter = ['capacity']
    search_fields = ['name']


@register(Product)
class ProductAdmin(ModelAdmin):
    pass


@register(Shipment)
class ShipmentAdmin(ModelAdmin):
    autocomplete_fields = ['vessel']
    date_hierarchy = 'laydaysstatement__laydaysdetail__interval_from'
    fieldsets = (
        (None, {'fields': (
            'number',
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
        'object_name',
        'buyer',
        'vessel',
        'dump_truck_trips',
        'tonnage',
        'balance',
        'ni',
        'fe',
        'moisture',
        'demurrage',
        'despatch',
        'completion',
        'number'
    )
    readonly_fields = ['number']
    search_fields = ['name', 'vessel__name']

    def get_queryset(self, request):
        qs = super().get_queryset(request) \
            .annotate(
                tonnage=F('laydaysstatement__tonnage'),
                ni=Round(F('shipmentloadingassay__ni'), 2),
                fe=Round(F('shipmentloadingassay__fe'), 2),
                moisture=Round(F('shipmentloadingassay__moisture'), 2),
                completion=F('laydaysstatement__completed_loading'),
                number=F('shipmentnumber__number')
            ) \
            .annotate(
                balance=Case(
                    When(completion__isnull=True, then=F('target_tonnage') - F('tonnage')),
                    output_field=IntegerField()
                )
            )
        return qs

    def balance(self, obj):
        return obj.balance

    def completion(self, obj):
        return obj.completion

    def fe(self, obj):
        return obj.fe

    def moisture(self, obj):
        return obj.moisture

    def ni(self, obj):
        return obj.ni

    def object_name(self, obj):
        return Shipment.objects.get(id=obj.id).name_html()

    def number(self, obj):
        return obj.number

    def tonnage(self, obj):
        return obj.tonnage

    fe.short_description = '%Fe'
    moisture.short_description = '%H₂O'
    ni.short_description = '%Ni'
    object_name.short_description = 'Name'


@register(Trip)
class TripAdmin(ModelAdmin):
    autocomplete_fields = ['lct', 'vessel']
    date_hierarchy = 'tripdetail__interval_from'
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
    list_filter = ['continuous', 'status', 'valid', 'lct']
    readonly_fields = ['valid', 'continuous', 'interval_from', 'interval_to']
    search_fields = ['lct__name', 'vessel__name']


@register(Vessel)
class VesselAdmin(ModelAdmin):
    exclude = ('stripped_name',)
    list_display = ('__str__',)
    search_fields = ['name']
