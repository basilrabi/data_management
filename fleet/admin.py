from django.contrib.admin import ModelAdmin, register

from .models.equipment import TrackedExcavator

@register(TrackedExcavator)
class TrackedExcavatorAdmin(ModelAdmin):
    pass
