from django.contrib.admin import ModelAdmin, TabularInline, register

# Register your models here.

from .models import MapDocumentControl, MapType, MinePlanningEngineer

@register(MapDocumentControl)
class MapDocumentControlAdmin(ModelAdmin):
    list_display = ('reference_map_no',
                    'date_created',
                    'material',
                    'ridge',
                    'year_on_map',
                    'month',
                    'company',
                    'map_uploads_img',
                    'map_creator',
                    'revision'
    )
    list_filter = ('map_type',
                   'ridge',
                   'company',
                   'month' 
    )
    readonly_fields=('number', 'revision',)

@register(MapType)
class MapTypeAdmin(ModelAdmin):
    pass

@register(MinePlanningEngineer)
class MinePlanningEngineerAdmin(ModelAdmin):
    pass