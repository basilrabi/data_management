from django.contrib.admin import ModelAdmin, TabularInline, register
from django.contrib.admin.views.main import ChangeList
from django.db.models import Count, TextField, Sum
from django.forms import Textarea
from import_export.admin import ExportMixin
from import_export.fields import Field
from import_export.resources import ModelResource

from custom.admin_gis import TMCLocationAdmin
from custom.filters import MineBlockListFilter
from sampling.models.proxy import DrillCore
from .models.equipment import EquipmentLocation
from .models.landuse import (
    Facility,
    FacilityClassification,
    FLA,
    MPSA,
    PEZA,
    RoadArea,
    WaterBody
)
from .models.source import Cluster, DrillHole, MineBlock, Stockpile


class ClusterResource(ModelResource):
    block_count = Field()

    class Meta:
        model = Cluster
        exclude = ('count', 'distance_from_road', 'id', 'geom', 'road')

    def dehydrate_block_count(self, cluster):
        return cluster.block_set.count()


class DrillCoreInline(TabularInline):
    model = DrillCore
    extra = 0
    fields = ('interval_from',
              'interval_to',
              'lithology',
              'lithology_modified',
              'description',
              'excavated_date',
              'ni',
              'fe',
              'co')
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={'rows':1, 'cols':40})}
    }
    readonly_fields = ['ni', 'fe', 'co']


class ClusterChangeList(ChangeList):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.blocks = self.queryset \
            .annotate(blocks=Count('block')) \
            .aggregate(Sum('blocks'))['blocks__sum']


@register(Cluster)
class ClusterAdmin(ExportMixin, ModelAdmin):
    date_hierarchy = 'date_scheduled'
    exclude = ('count', 'geom')
    list_display = ('name',
                    'blocks',
                    'mine_block',
                    'z',
                    'ni',
                    'fe',
                    'ore_class',
                    'date_scheduled',
                    'latest_layout_date',
                    'excavated')
    list_editable = ('date_scheduled',)
    list_filter = ['excavated',
                   'ore_class',
                   'date_scheduled',
                   'latest_layout_date',
                   MineBlockListFilter]
    readonly_fields = ['name',
                       'distance_from_road',
                       'road',
                       'excavated',
                       'z',
                       'ni',
                       'fe',
                       'co',
                       'mine_block',
                       'ore_class',
                       'date_scheduled',
                       'latest_layout_date']
    resource_class = ClusterResource
    search_fields = ['name', 'mine_block', 'z', 'ore_class']

    def get_changelist(self, request):
        return ClusterChangeList

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(blocks=Count('block'))
        return qs

    def blocks(self, obj):
        return obj.blocks


@register(DrillHole)
class DrillHoleAdmin(TMCLocationAdmin):
    modifiable = False
    inlines = [DrillCoreInline]
    list_display = ('name', 'date_drilled')
    search_fields = ['name']


@register(EquipmentLocation)
class EquipmentLocationAdmin(TMCLocationAdmin):
    date_hierarchy = 'time_stamp'
    modfiable = False
    readonly_fields = ['equipment', 'time_stamp']


@register(Facility)
class FacilityAdmin(TMCLocationAdmin):
    modifiable = False
    search_fields = [
        'name',
        'description',
        'classification__name',
        'classification__description'
    ]


@register(FacilityClassification)
class FacilityClassificationAdmin(ModelAdmin):
    search_fields = ['name', 'description']


@register(FLA)
class FLAAdmin(TMCLocationAdmin):
    modifiable = False
    search_fields = ['name']


@register(MineBlock)
class MineBlockAdmin(TMCLocationAdmin):
    modifiable = False
    list_display = ('name', 'ridge')
    search_fields = ['name']


@register(MPSA)
class MPSAAdmin(TMCLocationAdmin):
    modifiable = False
    search_fields = ['name']


@register(PEZA)
class PEZAAdmin(TMCLocationAdmin):
    modifiable = False
    search_fields = ['name']


@register(RoadArea)
class RoadAreaAdmin(TMCLocationAdmin):
    modifiable = False


@register(Stockpile)
class StockpileAdmin(TMCLocationAdmin):
    pass


@register(WaterBody)
class WaterBodyAdmin(TMCLocationAdmin):
    modifiable = False
    search_fields = ['name']
