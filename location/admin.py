from django.contrib.gis import admin
from .models.source import MineBlock, Stockyard

@admin.register(MineBlock)
class MineBlockAdmin(admin.ModelAdmin):
    exclude = ('geom',)
    list_display = ('name', 'ridge')

@admin.register(Stockyard)
class StockyardAdmin(admin.ModelAdmin):
    exclude = ('geom',)
    list_display = ('name', 'ridge')
