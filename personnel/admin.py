from django.contrib import admin

from .models.person import Designation, EmploymentRecord, Person

class EmploymentRecordInline(admin.TabularInline):
    model = EmploymentRecord
    extra = 0

@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    pass

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = [EmploymentRecordInline]
    list_display = ('__str__', 'present_designation')
