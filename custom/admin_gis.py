from django.contrib.gis.admin import GISModelAdmin
from django.contrib.gis.forms import OSMWidget


class TMCLocationWidget(OSMWidget):
    default_lon = 125.8313
    default_lat = 9.5235
    default_zoom = 14
    map_height = 600
    map_width = 800
    template_name = 'custom/map-topo.html'

    class Media:
        extend = False
        css = {
            'all': (
                'custom/css/ol.css',
                'gis/css/ol3.css',
            )
        }
        js = (
            'custom/js/ol.js',
            'gis/js/OLMapWidget.js',
        )


class TMCLocationAdmin(GISModelAdmin):
    gis_widget = TMCLocationWidget
