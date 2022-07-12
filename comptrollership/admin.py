from django.contrib.admin import ModelAdmin, register

from .models import (
    CostCenter,
    CostCenterConversion,
    GeneralLedgerAccount,
    SapCostCenter
)


@register(CostCenter)
class CostCenterAdmin(ModelAdmin):
    search_fields = ['name', 'description']


@register(CostCenterConversion)
class CostCenterConversionAdmin(ModelAdmin):
    search_fields = [
        'old_cost_center__name',
        'old_cost_center__description',
        'sap_cost_center__name',
        'sap_cost_center__description'
    ]


@register(GeneralLedgerAccount)
class GeneralLedgerAccountAdmin(ModelAdmin):
    search_fields = ['code', 'description']


@register(SapCostCenter)
class SapCostCenterAdmin(ModelAdmin):
    search_fields = ['name', 'description']
