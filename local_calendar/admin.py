from django.contrib.admin import ModelAdmin, register

from .models import Holiday, HolidayEvent


@register(Holiday)
class HolidayAdmin(ModelAdmin):
    autocomplete_fields = ['event']
    date_hierarchy = 'date'
    list_display = ['__str__', 'type']
    search_fields = ['event__name']


@register(HolidayEvent)
class HolidayEventAdmin(ModelAdmin):
    search_fields = ['name']
