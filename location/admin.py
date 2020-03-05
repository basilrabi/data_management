from django.contrib import admin

from custom.admin_gis import TMCLocationAdmin
from sampling.models.proxy import DrillCore
from .models.landuse import RoadArea
from .models.source import Cluster, DrillHole, MineBlock, Stockyard

class DrillCoreInline(admin.TabularInline):
    model = DrillCore
    extra = 0

@admin.register(Cluster)
class ClusterAdmin(TMCLocationAdmin):
    modifiable = False
    list_display = ('name',
                    'ni',
                    'fe',
                    'ore_class',
                    'with_layout',
                    'excavated')
    list_filter = ['with_layout', 'excavated']
    readonly_fields = ['z', 'ni', 'fe', 'co', 'mine_block', 'ore_class']
    search_fields = ['name', 'mine_block', 'z', 'ore_class']

@admin.register(DrillHole)
class DrillHoleAdmin(TMCLocationAdmin):
    modifiable = False
    inlines = [DrillCoreInline]
    list_display = ('name', 'date_drilled')

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
