from django.contrib import admin
from .models import BillingTracker, BillingAddOn
from django.db.models import TextField
from django.forms import Textarea

# Register your models here.

class BillingAddOnInline(admin.TabularInline):
    model = BillingAddOn
    extra = 0
    formfield_overrides = {
        TextField : {'widget': Textarea(attrs={'rows':1, 'cols':40})}
        }


class BillingTrackerAdmin(admin.ModelAdmin):
    inlines = [
        BillingAddOnInline
        ]

    list_display = ['contractor', 'purpose', 'start_date', 
                    'end_date', 'amount','specification', 'invoice_number','last_update']
    list_filter = ['purpose', 'contractor', 'last_update', 'start_date', 
                    'end_date', 'specification']



admin.site.register(BillingTracker, BillingTrackerAdmin)
