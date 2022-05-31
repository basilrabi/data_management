from django.contrib.admin import ModelAdmin, TabularInline, register
from django.db.models import F

from custom.models import User
from personnel.models.person import Person
from shipment.models.dso import Shipment
from .models.piling import PilingMethod, TripsPerPile
from .models.proxy import (
    AcquiredMiningSample,
    ChinaShipmentAssay,
    MiningSampleAssay,
    PamcoShipmentAssay
)
from .models.sample import (
    ApprovedShipmentDischargeAssay,
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


class MiningSampleIncrementInline(TabularInline):
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


class ShipmentDischargeLotAssayInline(TabularInline):
    model = ShipmentDischargeLotAssay
    extra = 0
    fields = ('lot', 'wmt', 'moisture', 'ni', 'dmt', 'ni_ton')
    readonly_fields = ('dmt', 'ni_ton')


class ShipmentLoadingLotAssayInline(ShipmentDischargeLotAssayInline):
    model = ShipmentLoadingLotAssay


class TripsPerPileInline(TabularInline):
    model = TripsPerPile
    extra = 0


@register(AcquiredMiningSample)
class AcquiredMiningSampleAdmin(ModelAdmin):
    list_display = ('__str__',
                    'dumping_area',
                    'trips',
                    'ready_for_delivery')
    exclude = ('ridge',
               'start_collection',
               'end_collection',
               'trips',
               'ready_for_delivery')


@register(ApprovedShipmentDischargeAssay)
class ApprovedShipmentDischargeAssayAdmin(ModelAdmin):
    date_hierarchy = 'assay__shipment__laydaysstatement__laydaysdetail__interval_from'
    list_display = ('object_name',
                    'number',
                    'vessel',
                    'approved',
                    'approved_certificate')
    readonly_fields = ('number',
                       'al2o3',
                       'arsenic',
                       'cao',
                       'co',
                       'cr',
                       'cr2o3',
                       'cu',
                       'dmt',
                       'fe',
                       'ignition_loss',
                       'k',
                       'laboratory',
                       'mgo',
                       'mn',
                       'moisture',
                       'ni',
                       'ni_ton',
                       'object_name',
                       'p',
                       'pb',
                       's',
                       'shipment',
                       'sio2',
                       'vessel',
                       'wmt',
                       'zn')
    search_fields = ['assay__shipment__name', 'assay__shipment__vessel__name']

    def add_view(self, request, form_url='', extra_context=None):
        self.fields = ('assay',)
        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        assay = ApprovedShipmentDischargeAssay.objects.get(id=object_id)
        if assay.assay.laboratory.name != 'PAMCO':
            self.fields = ('shipment',
                           'number',
                           'vessel',
                           'laboratory',
                           'wmt',
                           'dmt',
                           'moisture',
                           'al2o3',
                           'arsenic',
                           'cao',
                           'co',
                           'cr2o3',
                           'cu',
                           'fe',
                           'k',
                           'mgo',
                           'mn',
                           'ni',
                           'p',
                           'pb',
                           's',
                           'sio2',
                           'zn',
                           'ignition_loss',
                           'approved')
        else:
            self.fields = ('object_name',
                           'number',
                           'vessel',
                           'wmt',
                           'moisture',
                           'dmt',
                           'ni',
                           'ni_ton',
                           'co',
                           'cr',
                           'mn',
                           'fe',
                           'sio2',
                           'cao',
                           'mgo',
                           'al2o3',
                           'p',
                           's',
                           'ignition_loss',
                           'approved')
        self.fields += ('certificate',)
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )

    def get_queryset(self, request):
        qs = super().get_queryset(request).annotate(
            al2o3=F('assay__al2o3'),
            arsenic=F('assay__arsenic'),
            cao=F('assay__cao'),
            co=F('assay__co'),
            cr=F('assay__cr'),
            cr2o3=F('assay__cr2o3'),
            cu=F('assay__cu'),
            dmt=F('assay__dmt'),
            fe=F('assay__fe'),
            ignition_loss=F('assay__ignition_loss'),
            k=F('assay__k'),
            laboratory=F('assay__laboratory__name'),
            mgo=F('assay__mgo'),
            mn=F('assay__mn'),
            moisture=F('assay__moisture'),
            ni=F('assay__ni'),
            ni_ton=F('assay__ni_ton'),
            number=F('assay__shipment__shipmentnumber__number'),
            p=F('assay__p'),
            pb=F('assay__pb'),
            s=F('assay__s'),
            shipment=F('assay__shipment__name'),
            sio2=F('assay__sio2'),
            vessel=F('assay__shipment__vessel__name'),
            wmt=F('assay__wmt'),
            zn=F('assay__zn')
        )
        return qs

    def al2o3(self, obj):
        return obj.al2o3

    def arsenic(self, obj):
        return obj.arsenic

    def cao(self, obj):
        return obj.cao

    def co(self, obj):
        return obj.co

    def cr(self, obj):
        return obj.cr

    def cr2o3(self, obj):
        return obj.cr2o3

    def cu(self, obj):
        return obj.cu

    def dmt(self, obj):
        if obj.dmt:
            return f'{obj.dmt:,}'

    def fe(self, obj):
        return obj.fe

    def ignition_loss(self, obj):
        return obj.ignition_loss

    def k(self, obj):
        return obj.k

    def laboratory(self, obj):
        return obj.laboratory

    def mgo(self, obj):
        return obj.mgo

    def mn(self, obj):
        return obj.mn

    def moisture(self, obj):
        return obj.moisture

    def ni(self, obj):
        return obj.ni

    def ni_ton(self, obj):
        return obj.ni_ton

    def number(self, obj):
        return obj.number

    def object_name(self, obj):
        return ApprovedShipmentDischargeAssay.objects.get(id=obj.id).assay.shipment.name_html()

    def p(self, obj):
        return obj.p

    def pb(self, obj):
        return obj.pb

    def s(self, obj):
        return obj.s

    def shipment(self, obj):
        return obj.shipment

    def sio2(self, obj):
        return obj.sio2

    def vessel(self, obj):
        return obj.vessel

    def wmt(self, obj):
        if obj.wmt:
            return f'{obj.wmt:,}'

    def zn(self, obj):
        return obj.zn

    al2o3.short_description = '%Al₂O₃'
    arsenic.short_description = '%As'
    cao.short_description = '%CaO'
    co.short_description = '%Co'
    cr.short_description = '%Cr'
    cr2o3.short_description = '%Cr₂O₃'
    cu.short_description = '%Cu'
    dmt.short_description = 'DMT'
    fe.short_description = '%Fe'
    ignition_loss.short_description = '%LOI'
    k.short_description = '%K'
    mgo.short_description = '%MgO'
    mn.short_description = '%Mn'
    moisture.short_description = '%H₂O'
    ni.short_description = '%Ni'
    object_name.short_description = 'Shipment'
    p.short_description = '%P'
    pb.short_description = '%Pb'
    s.short_description = '%S'
    sio2.short_description = '%SiO₂'
    wmt.short_description = 'WMT'
    zn.short_description = '%Zn'


@register(ApprovedShipmentLoadingAssay)
class ApprovedShipmentLoadingAssayAdmin(ModelAdmin):
    date_hierarchy = 'assay__shipment__laydaysstatement__laydaysdetail__interval_from'
    list_display = (
        '__str__', 'number', 'vessel', 'approved', 'PDF', 'approved_certificate'
    )
    fields = ('assay', 'number', 'approved', 'certificate')
    readonly_fields = ('assay', 'number')
    search_fields = ['assay__shipment__name', 'assay__shipment__vessel__name']

    def get_queryset(self, request):
        qs = super().get_queryset(request).annotate(
            number=F('assay__shipment__shipmentnumber__number'),
            vessel=F('assay__shipment__vessel__name')
        )
        return qs

    def number(self, obj):
        return obj.number

    def vessel(self, obj):
        return obj.vessel


@register(ChinaShipmentAssay)
class ChinaShipmentAssayAdmin(ModelAdmin):
    autocomplete_fields = ['shipment']
    date_hierarchy = 'shipment__laydaysstatement__laydaysdetail__interval_from'
    list_display = ('__str__', 'number', 'vessel')
    readonly_fields = ('number', 'vessel')
    search_fields = ['shipment__name', 'shipment__vessel__name']

    def add_view(self, request, form_url='', extra_context=None):
        self.fields = ('shipment', 'laboratory')
        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.fields = ('shipment',
                       'number',
                       'vessel',
                       'laboratory',
                       'wmt',
                       'dmt',
                       'moisture',
                       'al2o3',
                       'arsenic',
                       'cao',
                       'co',
                       'cr2o3',
                       'cu',
                       'fe',
                       'k',
                       'mgo',
                       'mn',
                       'ni',
                       'p',
                       'pb',
                       's',
                       'sio2',
                       'zn',
                       'ignition_loss')
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'laboratory':
            kwargs["queryset"] = Laboratory.objects.distinct().exclude(name='PAMCO')
        if db_field.name == 'shipment':
            kwargs["queryset"] = Shipment.objects.distinct().filter(
                destination__name__contains='CHINA'
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request).exclude(laboratory__name='PAMCO') \
            .annotate(
                number=F('shipment__shipmentnumber__number'),
                vessel=F('shipment__vessel__name')
            )
        return qs

    def number(self, obj):
        return obj.number

    def vessel(self, obj):
        return obj.vessel


@register(Laboratory)
class LaboratoryAdmin(ModelAdmin):
    search_fields = ['name']


@register(Lithology)
class LithologyAdmin(ModelAdmin):
    pass


@register(MiningSampleAssay)
class MiningSampleAssayAdmin(ModelAdmin):
    list_display = ('__str__',
                    'date_received_for_preparation',
                    'date_prepared',
                    'date_received_for_analysis',
                    'date_analyzed')


@register(MiningSampleReport)
class MiningSampleReportAdmin(ModelAdmin):
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


@register(PamcoShipmentAssay)
class PamcoShipmentAssayAdmin(ModelAdmin):
    autocomplete_fields = ['shipment']
    date_hierarchy = 'shipment__laydaysstatement__laydaysdetail__interval_from'
    fields = ('shipment',
              'number',
              'vessel',
              'wmt',
              'dmt',
              'moisture',
              'ni',
              'ni_ton',
              'co',
              'cr',
              'mn',
              'fe',
              'sio2',
              'cao',
              'mgo',
              'al2o3',
              'p',
              's',
              'ignition_loss')
    inlines = [ShipmentDischargeLotAssayInline]
    list_display = ('object_name', 'number', 'vessel')
    readonly_fields = ('number', 'vessel')
    search_fields = ['shipment__name', 'shipment__vessel__name']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'shipment':
            kwargs["queryset"] = Shipment.objects.distinct().filter(
                destination__name__contains='JAPAN'
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request).filter(laboratory__name='PAMCO') \
            .annotate(
                number=F('shipment__shipmentnumber__number'),
                vessel=F('shipment__vessel__name')
            )
        return qs

    def object_name(self, obj):
        return PamcoShipmentAssay.objects.get(id=obj.id).shipment.name_html()

    def number(self, obj):
        return obj.number

    def vessel(self, obj):
        return obj.vessel

    object_name.short_description = 'Shipment'


@register(PilingMethod)
class PilingMethodAdmin(ModelAdmin):
    inlines = [TripsPerPileInline]
    list_display = ('name', 'present_required_trip')


@register(ShipmentLoadingAssay)
class ShipmentLoadingAssayAdmin(ModelAdmin):
    autocomplete_fields = ['shipment']
    date_hierarchy = 'shipment__laydaysstatement__laydaysdetail__interval_from'
    list_display = ('object_name',
                    'number',
                    'vessel',
                    'approved',
                    'PDF',
                    'approved_certificate')
    readonly_fields = ('wmt', 'dmt', 'moisture', 'ni', 'ni_ton', 'number')
    search_fields = ['shipment__name', 'shipment__vessel__name']

    def add_view(self, request, form_url='', extra_context=None):
        self.fields = ('date', 'shipment', 'chemist')
        self.inlines = []
        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        assay = ShipmentLoadingAssay.objects.get(id=object_id)
        self.fields = ('number',
                       'date',
                       'shipment',
                       'chemist',
                       'wmt',
                       'dmt',
                       'moisture',
                       'ni',
                       'ni_ton',
                       'fe',
                       'mgo',
                       'sio2',
                       'cr',
                       'co')
        if assay.shipment.product.name == 'LIMONITE':
            self.fields += ('al2o3',)
        self.inlines = [ShipmentLoadingLotAssayInline]
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'chemist':
            kwargs["queryset"] = User.objects.filter(groups__name='chemist')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request) \
            .annotate(
                approved=F('approvedshipmentloadingassay__approved'),
                number=F('shipment__shipmentnumber__number'),
                vessel=F('shipment__vessel__name')
            )
        return qs

    def approved(self, obj):
        return obj.approved

    def number(self, obj):
        return obj.number

    def object_name(self, obj):
        return ShipmentLoadingAssay.objects.get(id=obj.id).shipment.name_html()

    def vessel(self, obj):
        return obj.vessel

    approved.admin_order_field = 'approved'
    approved.boolean = True
    object_name.short_description = 'Shipment'
