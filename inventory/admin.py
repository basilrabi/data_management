from django.contrib.admin import register

from custom.admin_gis import TMCLocationAdmin
from .models.insitu import Block, DrillArea


@register(Block)
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


@register(DrillArea)
class DrillAreaAdmin(TMCLocationAdmin):
    modifiable = False
