from django.contrib.admin import ModelAdmin, TabularInline, register
from django.db.models import TextField
from django.forms import Textarea

from .forms import CMBillingForm, ShipmentBillingForm
from .models import BillingTracker, BillingAddOn, CMBilling, ShipmentBilling


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
    form = CMBillingForm
    list_display = ['contractor',
                    'month',
                    'half',
                    'billing_year',
                    'amount',
                    'tonnage',
                    'last_update']
    list_filter = ['contractor']


@register(ShipmentBilling)
class ShipmentBillingAdmin(ModelAdmin):
    form = ShipmentBillingForm
    list_display = ['contractor',
                    'shipment',
                    'amount',
                    'tonnage',
                    'last_update']
                    