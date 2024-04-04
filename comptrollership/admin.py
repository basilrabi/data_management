from django.contrib.admin import ModelAdmin, register

from .models import (
    ActivityCategory,
    ActivityCode,
    CostCenter,
    CostCenterConversion,
    GeneralLedgerAccount,
    Material,
    MonthlyCost,
    OperationHead,
    ProfitCenter,
    SapCostCenter
)


@register(ActivityCategory)
class ActivityCategoryAdmin(ModelAdmin):
    search_fields = ['description', 'name']
    list_display = ('name', 'description')


@register(ActivityCode)
class ActivityCodeAdmin(ModelAdmin):
    search_fields = ['description', 'name']
    list_display = ('name', 'description')


@register(CostCenter)
class CostCenterAdmin(ModelAdmin):
    search_fields = ['description', 'name']
    list_display = ('name', 'description', 'material')
    list_editable = ('description', 'material')
    list_filter = ['material',]


@register(CostCenterConversion)
class CostCenterConversionAdmin(ModelAdmin):
    autocomplete_fields = ['old_cost_center', 'sap_cost_center']
    list_display = (
        '__str__',
        'operation_code',
        'with_contract',
        'with_inhouse',
        'with_rental',
        'operation_head',
        'activity_code',
        'activity_category'
    )
    list_editable = (
        'activity_category',
        'activity_code',
        'operation_code',
        'operation_head',
        'with_contract',
        'with_inhouse',
        'with_rental',
    )
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


@register(Material)
class MaterialAdmin(ModelAdmin):
    search_fields = ['description', 'name']
    list_display = ('name', 'description')


@register(MonthlyCost)
class MonthlyCostAdmin(ModelAdmin):
    list_display = (
        '__str__', 'budget', 'adjusted_budget', 'forecast', 'actual'
    )
    list_filter = ['year', 'month']
    readonly_fields = ['year',
                       'month',
                       'cost_center',
                       'gl',
                       'actual',
                       'adjusted_budget',
                       'budget',
                       'forecast']
    search_fields = [
        'cost_center__name',
        'cost_center__description',
        'gl__code',
        'gl__description'
    ]


@register(OperationHead)
class OperationHeadAdmin(ModelAdmin):
    search_fields = ['description', 'name']
    list_display = ('name', 'description')


@register(ProfitCenter)
class ProfitCenterAdmin(ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ['description', 'name']


@register(SapCostCenter)
class SapCostCenterAdmin(ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ['description', 'long_name', 'name']

