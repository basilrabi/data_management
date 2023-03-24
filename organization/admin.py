from django.contrib.admin import ModelAdmin, register
from nested_admin import NestedTabularInline, NestedModelAdmin

from .models import Department, Division, Organization, Section


@register(Organization)
class OrganizationAdmin(ModelAdmin):
    list_display = ('name', 'description', 'service', 'active')


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