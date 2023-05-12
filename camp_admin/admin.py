from django.contrib.admin import(
    ModelAdmin, 
    register, 
    TabularInline
)

from .models import(
    Comprehensive,
    CTPL,
    Floater,
    VehicularInsurance
)


class CTPLInline(TabularInline):
    model = CTPL
    extra = 0


class ComprehensiveInline(TabularInline):
    model = Comprehensive
    extra = 0


class FloaterInline(TabularInline):
    model = Floater
    extra = 0


@register(VehicularInsurance)
class VehicularInsuranceAdmin(ModelAdmin):
    inlines = [CTPLInline, ComprehensiveInline, FloaterInline]
    list_display = ['equipment', 'ctpl_expiry_date', 'comprehensive_expiry_date', 'floater_expiry_date']


    def ctpl_expiry_date(self, obj):
        ctpl = CTPL.objects.filter(equipment=obj).last()
        if ctpl:
            return ctpl.date_expiry
        else:
            return None
    ctpl_expiry_date.short_description = 'CTPL Expiry'

    def comprehensive_expiry_date(self, obj):
        comprehensive = Comprehensive.objects.filter(equipment=obj).last()
        if comprehensive:
            return comprehensive.date_expiry
        else:
            return None
    comprehensive_expiry_date.short_description = 'Comprehensive Expiry'

    def floater_expiry_date(self, obj):
        floater = Floater.objects.filter(equipment=obj).last()
        if floater:
            return floater.date_expiry
        else:
            return None
    floater_expiry_date.short_description = 'Floater Expiry'