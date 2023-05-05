from django.contrib.admin import ModelAdmin, register

from .models import (
    CostCenter,
    CostCenterConversion,
    GeneralLedgerAccount,
    MonthlyCost,
    ProfitCenter,
    SapCostCenter
)


@register(CostCenter)
class CostCenterAdmin(ModelAdmin):
    search_fields = ['description', 'name']
    list_display = ('name', 'description')


@register(CostCenterConversion)
class CostCenterConversionAdmin(ModelAdmin):
    autocomplete_fields = ['old_cost_center', 'sap_cost_center']
    search_fields = [
        'old_cost_center__name',
        'old_cost_center__description',
        'sap_cost_center__name',
        'sap_cost_center__description'
    ]


@register(GeneralLedgerAccount)
class GeneralLedgerAccountAdmin(ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ['code', 'description']


@register(MonthlyCost)
class MonthlyCostAdmin(ModelAdmin):
    list_display = (
        '__str__', 'budget', 'adjusted_budget', 'forecast', 'actual'
    )
    list_filter = ['year', 'month']
    search_fields = [
        'cost_center__name',
        'cost_center__description',
        'gl__code',
        'gl__description'
    ]


@register(ProfitCenter)
class ProfitCenterAdmin(ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ['description', 'name']


@register(SapCostCenter)
class SapCostCenterAdmin(ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ['description', 'long_name', 'name']
