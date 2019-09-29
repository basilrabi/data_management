from django.contrib.gis import admin

class TMCLocationAdmin(admin.GeoModelAdmin):
    default_lon = 125.8313
    default_lat = 9.5235
    default_zoom = 14
    wms_name = 'TMC'
    wms_url = 'http://192.169.101.192:8010/ogc/map'
    wms_layer = 'Taganito Mine General Location'
    num_zoom = 25
    openlayers_url = 'http://192.169.101.192:81/static/OpenLayers-2.13.1/OpenLayers.js'
