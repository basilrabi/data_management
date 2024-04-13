from django.contrib.admin import ModelAdmin, register
from nested_admin import NestedTabularInline, NestedModelAdmin

from .models import (
    Department,
    Division,
    ManilaGpsApiKey,
    Organization,
    Section,
    ServiceProvider
)


class SectionInline(NestedTabularInline):
    model = Section
    extra = 0


class DepartmentInline(NestedTabularInline):
    model = Department
    extra = 0
    inlines = [SectionInline]


@register(Division)
class DivisionAdmin(NestedModelAdmin):
    inlines = [DepartmentInline]


@register(ManilaGpsApiKey)
class ManilaGpsApiKeyAdmin(ModelAdmin):
    list_display = ('owner', 'key')


@register(Organization)
class OrganizationAdmin(ModelAdmin):
    list_display = ('name', 'description', 'service', 'active')
    search_fields = ['description', 'name', 'service']

    # TODO: modify jquery GET REQUEST when being requested in ProviderEquipment
    # as foreign key. What should be fetched are only contractors.


@register(ServiceProvider)
class ServiceProviderAdmin(ModelAdmin):
    list_display = ('name', 'description', 'active')
    search_fields = ['description', 'name']

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request,
            queryset,
            search_term,
        )
        try:
            queryset = queryset.filter(service='Contractor')
        except:
            pass
        return queryset, may_have_duplicates

