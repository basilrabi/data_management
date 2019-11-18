from django.contrib import admin
from custom.admin_gis import TMCLocationAdmin
from .models.source import MineBlock, Stockyard

@admin.register(MineBlock)
class MineBlockAdmin(TMCLocationAdmin):
    modifiable = False
    list_display = ('name', 'ridge')

@admin.register(Stockyard)
class StockyardAdmin(TMCLocationAdmin):
    pass
