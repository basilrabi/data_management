from django.contrib import admin
from django.db import models
from django.forms import Textarea

from custom.admin_gis import TMCLocationAdmin
from sampling.models.proxy import DrillCore
from .models.landuse import RoadArea
from .models.source import Cluster, DrillHole, MineBlock, Stockyard

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

@admin.register(Cluster)
class ClusterAdmin(TMCLocationAdmin):
    modifiable = False
    exclude = ('count',)
    list_display = ('name',
                    'mine_block',
                    'z',
                    'ni',
                    'fe',
                    'ore_class',
                    'date_scheduled',
                    'layout_date',
                    'excavated')
    list_editable = ('date_scheduled',)
    list_filter = ['excavated', 'ore_class', 'mine_block']
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
    search_fields = ['name', 'mine_block', 'z', 'ore_class']

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
