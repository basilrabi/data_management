from django.contrib import admin
from custom.admin_gis import TMCLocationAdmin
from .models.insitu import Block

@admin.register(Block)
class BlockAdmin(TMCLocationAdmin):
    modifiable = False
    list_display = ('name',
                    'z',
                    'ni',
                    'fe',
                    'co',
                    'excavated')
    readonly_fields = ['name',
                       'cluster',
                       'z',
                       'ni',
                       'fe',
                       'co']
    search_fields = ['name']
