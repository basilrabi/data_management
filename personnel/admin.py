from django.contrib.admin import ModelAdmin, TabularInline, register

from .models.person import Designation, EmploymentRecord, Person


class EmploymentRecordInline(TabularInline):
    model = EmploymentRecord
    extra = 0


@register(Designation)
class DesignationAdmin(ModelAdmin):
    pass


@register(Person)
class PersonAdmin(ModelAdmin):
    inlines = [EmploymentRecordInline]
    list_display = ('__str__', 'present_designation')
