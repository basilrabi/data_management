from django.contrib import admin

from custom.admin_gis import TMCLocationAdmin
from .models.insitu import Block, DrillArea

@admin.register(Block)
class BlockAdmin(TMCLocationAdmin):
    modifiable = False
    list_display = ('name',
                    'z',
                    'ni',
                    'fe',
                    'co')
    readonly_fields = ['name',
                       'cluster',
                       'z',
                       'ni',
                       'fe',
                       'co',
                       'depth']
    search_fields = ['name']

@admin.register(DrillArea)
class DrillAreaAdmin(TMCLocationAdmin):
    modifiable = False
