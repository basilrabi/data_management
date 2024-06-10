from copy import deepcopy
from django.contrib.admin import ModelAdmin, TabularInline, helpers, register
from django.contrib.admin.utils import flatten_fieldsets, unquote
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
from django.forms.formsets import all_valid
from django.forms.models import BaseInlineFormSet
from django.utils.translation import gettext as _
from import_export.admin import ExportMixin
from import_export.fields import Field
from import_export.resources import ModelResource

from custom.functions import Round
from custom.functions_standalone import print_tz_manila
from location.models.shipment import Anchorage
from .models.lct import LCT, LCTContract, Trip, TripDetail
from .models.dso import (
    ApprovedLayDaysStatement,
    Buyer,
    Destination,
    DraftSurvey,
    LayDaysDetail,
    LayDaysStatement,
    Product,
    Shipment,
    Vessel,
)
from .models.proxy import FinalShipmentDetail


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


class LCTContractInline(TabularInline):
    model = LCTContract
    extra = 0


class LayDaysDetailInline(TabularInline):
    model = LayDaysDetail
    extra = 0
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={'rows':1, 'cols':40})}
    }
    formset = IntervalFromInlineFormSet


class TripDetailInline(TabularInline):
    model = TripDetail
    extra = 0
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={'rows':1, 'cols':40})}
    }
    formset = IntervalFromInlineFormSet


@register(ApprovedLayDaysStatement)
class ApprovedLayDaysStatementAdmin(ModelAdmin):
    list_display = ('object_name', 'number', 'vessel', 'approved', 'signed_statement')
    readonly_fields = ['number', 'statement', 'despatch']
    search_fields = ['statement__shipment__name',
                     'statement__shipment__vessel__name']

    def get_queryset(self, request):
        qs = super().get_queryset(request).annotate(
            vessel=F('statement__shipment__vessel__name')
        )
        return qs

    def object_name(self, obj):
        return ApprovedLayDaysStatement.objects.get(id=obj.id).statement.shipment.name_html()

    def vessel(self, obj):
        return obj.vessel

    object_name.short_description = 'Shipment'


@register(Buyer)
class BuyerAdmin(ModelAdmin):
    search_fields = ['name']


@register(Destination)
class DestinationAdmin(ModelAdmin):
    search_fields = ['name']


@register(DraftSurvey)
class DraftSurveyAdmin(ModelAdmin):
    date_hierarchy = 'shipment__laydaysstatement__laydaysdetail__interval_from'
    list_display = ['shipment',
                    'video',
                    'images_in_pdf',
                    'mgb_receipt']
    search_fields = ['shipment__name']


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
    search_fields = ['name', 'product__name', 'vessel__name']

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


@register(LCT)
class LCTAdmin(ModelAdmin):
    inlines = [LCTContractInline]
    list_display = ('name', 'capacity')
    list_filter = ['capacity']
    search_fields = ['name']


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
        'approved',
        'difference_with_assay'
    )
    readonly_fields = [
        'approved',
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
    search_fields = ['shipment__name', 'shipment__vessel__name']

    def get_queryset(self, request):
        qs = super().get_queryset(request).annotate(
            difference_with_assay=F('shipment__shipmentloadingassay__wmt') - F('tonnage')
        )
        return qs

    def difference_with_assay(self, obj):
        return obj.difference_with_assay

    def object_name(self, obj):
        return LayDaysStatement.objects.get(id=obj.id).shipment.name_html()

    difference_with_assay.admin_order_field= 'difference_with_assay'
    object_name.short_description = 'Shipment'


@register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('__str__', 'ni', 'fe', 'moisture')
    search_fields = ['name']


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
        'commenced_laytime',
        'completion',
        'number'
    )
    readonly_fields = ['number']
    search_fields = ['name', 'product__name', 'vessel__name']

    def get_queryset(self, request):
        qs = super().get_queryset(request) \
            .annotate(
                tonnage=F('laydaysstatement__tonnage'),
                ni=Round(F('shipmentloadingassay__ni'), 2),
                fe=Round(F('shipmentloadingassay__fe'), 2),
                moisture=Round(F('shipmentloadingassay__moisture'), 2),
                commenced_laytime=F('laydaysstatement__commenced_laytime'),
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

    def commenced_laytime(self, obj):
        return obj.commenced_laytime

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
    readonly_fields = ['valid', 'continuous', 'interval_from', 'interval_to', 'valid_vessels']
    search_fields = ['lct__name', 'vessel__name']

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = []
        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = [TripDetailInline]
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )

    def _changeform_view(self, request, object_id, form_url, extra_context):
        """
        Temporarily override _chageform_view to address #249.
        TODO: Drop this override once the root cause of #249 is identified.
        """
        IS_POPUP_VAR = "_popup"
        TO_FIELD_VAR = "_to_field"
        to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
        if to_field and not self.to_field_allowed(request, to_field):
            raise DisallowedModelAdminToField(
                "The field %s cannot be referenced." % to_field
            )

        if request.method == "POST" and "_saveasnew" in request.POST:
            object_id = None

        add = object_id is None

        if add:
            if not self.has_add_permission(request):
                raise PermissionDenied
            obj = None

        else:
            obj = self.get_object(request, unquote(object_id), to_field)

            if request.method == "POST":
                if not self.has_change_permission(request, obj):
                    raise PermissionDenied
            else:
                if not self.has_view_or_change_permission(request, obj):
                    raise PermissionDenied

            if obj is None:
                return self._get_obj_does_not_exist_redirect(
                    request, self.opts, object_id
                )

        fieldsets = self.get_fieldsets(request, obj)
        ModelForm = self.get_form(
            request, obj, change=not add, fields=flatten_fieldsets(fieldsets)
        )
        if request.method == "POST":
            form = ModelForm(request.POST, request.FILES, instance=obj)
            formsets, inline_instances = self._create_formsets(
                request,
                form.instance,
                change=not add,
            )
            form_validated = form.is_valid()
            if form_validated:
                # Create a deep copy instead to prevent reverting to the unmodified object when calling an element of formsets
                new_object = deepcopy(self.save_form(request, form, change=not add))
            else:
                new_object = form.instance
            if all_valid(formsets) and form_validated:
                self.save_model(request, new_object, form, not add)
                self.save_related(request, form, formsets, not add)
                change_message = self.construct_change_message(
                    request, form, formsets, add
                )
                if add:
                    self.log_addition(request, new_object, change_message)
                    return self.response_add(request, new_object)
                else:
                    self.log_change(request, new_object, change_message)
                    return self.response_change(request, new_object)
            else:
                form_validated = False
        else:
            if add:
                initial = self.get_changeform_initial_data(request)
                form = ModelForm(initial=initial)
                formsets, inline_instances = self._create_formsets(
                    request, form.instance, change=False
                )
            else:
                form = ModelForm(instance=obj)
                formsets, inline_instances = self._create_formsets(
                    request, obj, change=True
                )

        if not add and not self.has_change_permission(request, obj):
            readonly_fields = flatten_fieldsets(fieldsets)
        else:
            readonly_fields = self.get_readonly_fields(request, obj)
        admin_form = helpers.AdminForm(
            form,
            list(fieldsets),
            # Clear prepopulated fields on a view-only form to avoid a crash.
            (
                self.get_prepopulated_fields(request, obj)
                if add or self.has_change_permission(request, obj)
                else {}
            ),
            readonly_fields,
            model_admin=self,
        )
        media = self.media + admin_form.media

        inline_formsets = self.get_inline_formsets(
            request, formsets, inline_instances, obj
        )
        for inline_formset in inline_formsets:
            media += inline_formset.media

        if add:
            title = _("Add %s")
        elif self.has_change_permission(request, obj):
            title = _("Change %s")
        else:
            title = _("View %s")
        context = {
            **self.admin_site.each_context(request),
            "title": title % self.opts.verbose_name,
            "subtitle": str(obj) if obj else None,
            "adminform": admin_form,
            "object_id": object_id,
            "original": obj,
            "is_popup": IS_POPUP_VAR in request.POST or IS_POPUP_VAR in request.GET,
            "to_field": to_field,
            "media": media,
            "inline_admin_formsets": inline_formsets,
            "errors": helpers.AdminErrorList(form, formsets),
            "preserved_filters": self.get_preserved_filters(request),
        }

        # Hide the "Save" and "Save and continue" buttons if "Save as New" was
        # previously chosen to prevent the interface from getting confusing.
        if (
            request.method == "POST"
            and not form_validated
            and "_saveasnew" in request.POST
        ):
            context["show_save"] = False
            context["show_save_and_continue"] = False
            # Use the change template instead of the add template.
            add = False

        context.update(extra_context or {})

        return self.render_change_form(
            request, context, add=add, change=not add, obj=obj, form_url=form_url
        )


@register(Vessel)
class VesselAdmin(ModelAdmin):
    exclude = ('stripped_name',)
    list_display = ('__str__',)
    search_fields = ['name']
