from django.contrib.admin import ModelAdmin, register

from .models import Organization


@register(Organization)
class OrganizationAdmin(ModelAdmin):
    list_display = ('__str__', 'description')
