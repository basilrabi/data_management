from django.contrib.admin import register

from custom.admin import ReadOnlyAdmin
from .models import (
    LegacyGoodsIssuance,
    LegacyGoodsReceivedNote,
    LegacyItemType,
    LegacyMaterial,
    LegacyVendor
)


@register(LegacyGoodsIssuance)
class LegacyGoodsIssuanceAdmin(ReadOnlyAdmin):
    date_hierarchy = 'transaction_date'
    list_display = ('__str__', 'cost_center', 'equipment', 'quantity')
    search_fields = ['cost_center',
                     'equipment',
                     'material__name',
                     'material__item_type__name',
                     'order_type']


@register(LegacyGoodsReceivedNote)
class LegacyGoodsReceivedAdmin(ReadOnlyAdmin):
    date_hierarchy = 'transaction_date'
    list_display = ('__str__',
                    'purchase_order',
                    'vendor',
                    'quantity',
                    'total_price')
    search_fields = ['invoice_number',
                     'material__name',
                     'material__item_type__name',
                     'purchase_order',
                     'reference_number',
                     'vendor__name']


@register(LegacyItemType)
class LegacyItemTypeAdmin(ReadOnlyAdmin):
    search_fields = ['name']


@register(LegacyMaterial)
class LegacyMaterialTypeAdmin(ReadOnlyAdmin):
    list_display = ('__str__', 'description')
    search_fields = ['name', 'description']


@register(LegacyVendor)
class LegacyVendorAdmin(ReadOnlyAdmin):
    search_fields = ['name']
