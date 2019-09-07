from django.contrib import admin
from django.db import models
from django.forms import Textarea

from .models.lct import LCT, LCTContract, Trip, TripDetail
from .models.dso import LayDaysDetail, LayDaysStatement, Shipment, Vessel

class LayDaysDetailInline(admin.TabularInline):
    model = LayDaysDetail
    extra = 0

class LCTContractInline(admin.TabularInline):
    model = LCTContract
    extra = 0

class TripDetailInline(admin.StackedInline):
    model = TripDetail
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':40})}
    }

@admin.register(LayDaysStatement)
class LayDaysStatementAdmin(admin.ModelAdmin):
    inlines = [LayDaysDetailInline]
    readonly_fields = ['commenced_laytime',
                       'commenced_loading',
                       'completed_loading',
                       'time_allowed',
                       'time_used',
                       'demurrage',
                       'despatch']
    list_display = ('__str__',
                    'vessel',
                    'commenced_laytime',
                    'completed_loading',
                    'demurrage',
                    'despatch')

@admin.register(LCT)
class LCTAdmin(admin.ModelAdmin):
    inlines = [LCTContractInline]
    list_display = ('name', 'capacity')

@admin.register(Vessel)
class VesselAdmin(admin.ModelAdmin):
    pass

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'vessel', 'start_loading', 'end_loading', 'tonnage')

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    inlines = [TripDetailInline]
    readonly_fields = ['interval_from', 'interval_to']
    list_display = ('lct',
                    'interval_from',
                    'interval_to',
                    'vessel',
                    'dump_truck_trips',
                    'cycle',
                    'valid')
