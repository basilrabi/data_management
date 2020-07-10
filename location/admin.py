from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.db import models
from django.forms import Textarea
from import_export.admin import ExportMixin
from import_export.fields import Field
from import_export.resources import ModelResource

from custom.admin_gis import TMCLocationAdmin
from sampling.models.proxy import DrillCore
from .models.landuse import RoadArea
from .models.source import Cluster, DrillHole, MineBlock, Stockyard

class ClusterResource(ModelResource):
    cluster_count = Field()

    class Meta:
        model = Cluster
        exclude = ('count', 'distance_from_road', 'id', 'geom', 'road')

    def dehydrate_cluster_count(self, cluster):
        return cluster.block_set.count()

class DrillCoreInline(admin.TabularInline):
    model = DrillCore
    exclude = ('al',
               'c',
               'cr',
               'mg',
               'sc',
               'si',
               'moisture',
               'date_received_for_preparation',
               'date_prepared',
               'date_received_for_analysis',
               'date_analyzed')
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':40})}
    }
    readonly_fields = ['ni', 'fe', 'co']

class ClusterChangeList(ChangeList):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.blocks = self.queryset \
            .annotate(blocks=models.Count('block')) \
            .aggregate(models.Sum('blocks'))['blocks__sum']

@admin.register(Cluster)
class ClusterAdmin(ExportMixin, admin.ModelAdmin):
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
                    'layout_date',
                    'excavated')
    list_editable = ('date_scheduled',)
    list_filter = ['excavated',
                   'ore_class',
                   'date_scheduled',
                   'layout_date',
                   'mine_block']
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
                       'layout_date']
    resource_class = ClusterResource
    search_fields = ['name', 'mine_block', 'z', 'ore_class']

    def get_changelist(self, request):
        return ClusterChangeList

@admin.register(DrillHole)
class DrillHoleAdmin(TMCLocationAdmin):
    modifiable = False
    inlines = [DrillCoreInline]
    list_display = ('name', 'date_drilled')
    search_fields = ['name']

@admin.register(MineBlock)
class MineBlockAdmin(TMCLocationAdmin):
    modifiable = False
    list_display = ('name', 'ridge')

@admin.register(RoadArea)
class RoadAreaAdmin(TMCLocationAdmin):
    modifiable = False

@admin.register(Stockyard)
class StockyardAdmin(TMCLocationAdmin):
    pass
