from django.contrib.gis import admin
from .models.source import MineBlock, Stockyard

default_lon = 125.8313
default_lat = 9.5235
default_zoom = 14
wms_name = 'TMC'
wms_url = 'http://192.169.101.192:8010/ogc/map'
wms_layer = 'Taganito Mine General Location'
num_zoom = 25

@admin.register(MineBlock)
class MineBlockAdmin(admin.GeoModelAdmin):
    default_lon = default_lon
    default_lat = default_lat
    default_zoom = default_zoom
    wms_name = wms_name
    wms_url = wms_url
    wms_layer = wms_layer
    num_zoom = num_zoom
    modifiable = False
    list_display = ('name', 'ridge')

@admin.register(Stockyard)
class StockyardAdmin(admin.GeoModelAdmin):
    default_lon = default_lon
    default_lat = default_lat
    default_zoom = default_zoom
    wms_name = wms_name
    wms_url = wms_url
    wms_layer = wms_layer
    num_zoom = num_zoom
    list_display = ('name', 'ridge')
