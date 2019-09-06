from django.contrib import admin

from .models.equipment import TrackedExcavator

@admin.register(TrackedExcavator)
class TrackedExcavatorAdmin(admin.ModelAdmin):
    pass
