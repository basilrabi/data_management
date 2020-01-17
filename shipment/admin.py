from django.contrib import admin
from django.db import models
from django.forms import Textarea

from .models.lct import LCT, LCTContract, Trip, TripDetail
from .models.dso import LayDaysDetail, LayDaysStatement, Shipment, Vessel

class LayDaysDetailInline(admin.TabularInline):
    model = LayDaysDetail
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':40})}
    }

class LCTContractInline(admin.TabularInline):
    model = LCTContract
    extra = 0

class TripDetailInline(admin.TabularInline):
    model = TripDetail
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':40})}
    }

@admin.register(LayDaysStatement)
class LayDaysStatementAdmin(admin.ModelAdmin):
    autocomplete_fields = ['shipment']
    inlines = [LayDaysDetailInline]
    list_display = ('__str__',
                    'vessel',
                    'commenced_laytime',
                    'completed_loading',
                    'demurrage',
                    'despatch',
                    'PDF')
    list_filter = ['completed_loading']
    readonly_fields = ['date_saved',
                       'date_computed',
                       'commenced_laytime',
                       'commenced_loading',
                       'completed_loading',
                       'time_allowed',
                       'additional_laytime',
                       'demurrage',
                       'despatch']
    search_fields = ['shipment__name']

@admin.register(LCT)
class LCTAdmin(admin.ModelAdmin):
    inlines = [LCTContractInline]
    list_display = ('name', 'capacity')
    list_filter = ['capacity']
    search_fields = ['name']

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    autocomplete_fields = ['vessel']
    list_display = ('name', 'vessel', 'start_loading', 'end_loading', 'tonnage')
    search_fields = ['name', 'vessel__name']

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    autocomplete_fields = ['lct', 'vessel']
    inlines = [TripDetailInline]
    list_display = ('lct',
                    'interval_from',
                    'interval_to',
                    'vessel',
                    'dump_truck_trips',
                    'cycle',
                    'valid',
                    'continuous')
    list_filter = ['continuous', 'status', 'valid']
    readonly_fields = ['valid', 'continuous', 'interval_from', 'interval_to']
    search_fields = ['lct__name', 'vessel__name']

@admin.register(Vessel)
class VesselAdmin(admin.ModelAdmin):
    exclude = ('stripped_name',)
    list_display = ('__str__',)
    search_fields = ['name']
