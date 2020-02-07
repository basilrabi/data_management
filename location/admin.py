from django.contrib import admin
from custom.admin_gis import TMCLocationAdmin
from .models.source import Cluster, MineBlock, Stockyard

@admin.register(Cluster)
class ClusterAdmin(TMCLocationAdmin):
    modifiable = False
    list_display = ('name',
                    'ni',
                    'fe',
                    'co',
                    'with_layout',
                    'excavated')
    list_filter = ['with_layout', 'excavated']
    readonly_fields = ['ni', 'fe', 'co','mine_block']
    search_fields = ['name', 'mine_block', 'z']

@admin.register(MineBlock)
class MineBlockAdmin(TMCLocationAdmin):
    modifiable = False
    list_display = ('name', 'ridge')

@admin.register(Stockyard)
class StockyardAdmin(TMCLocationAdmin):
    pass
