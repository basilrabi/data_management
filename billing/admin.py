from datetime import datetime
from django.contrib.admin import ModelAdmin, TabularInline, register
from django.db.models import TextField
from django.forms import Textarea

from organization.models import Organization
from shipment.models.dso import LayDaysStatement
from .models import BillingTracker, BillingAddOn, CMBilling, ShipmentBilling, ShipmentBillingEntry


class BillingAddOnInline(TabularInline):
    model = BillingAddOn
    extra = 0
    formfield_overrides = {
        TextField : {'widget': Textarea(attrs={'rows':1, 'cols':40})}
    }


@register(BillingTracker)
class BillingTrackerAdmin(ModelAdmin):
    inlines = [BillingAddOnInline]
    list_display = ['contractor',
                    'purpose',
                    'start_date',
                    'end_date',
                    'amount',
                    'specification',
                    'invoice_number',
                    'last_update']
    list_filter = ['purpose',
                   'contractor',
                   'last_update',
                   'start_date',
                   'end_date',
                   'specification']


@register(CMBilling)
class CMBillingAdmin(ModelAdmin):
    list_display = ['contractor',
                    'month',
                    'half',
                    'billing_year',
                    'amount',
                    'tonnage',
                    'last_update']
    list_filter = ['contractor']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'contractor':
            kwargs['queryset'] = Organization.objects.filter(active=True, service='Contractor')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ShipmentBillingEntryInline(TabularInline):
    model = ShipmentBillingEntry
    extra = 0
    ordering = ['contractor']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'contractor':
            kwargs['queryset'] = Organization.objects.filter(active=True, service='Contractor')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@register(ShipmentBilling)
class ShipmentBillingAdmin(ModelAdmin):
    inlines = [ShipmentBillingEntryInline]
    list_display = ['shipment']
    ordering = ['-shipment']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'shipment':
            kwargs['queryset'] = LayDaysStatement.objects.filter(completed_loading__year=datetime.now().year)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

