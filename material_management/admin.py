from django.contrib.admin import ModelAdmin, register

from .models import (
    LegacyGoodsIssuance,
    LegacyGoodsReceivedNote,
    LegacyItemType,
    LegacyMaterial,
    LegacyVendor
)


@register(LegacyGoodsIssuance)
class LegacyGoodsIssuanceAdmin(ModelAdmin):
    date_hierarchy = 'transaction_date'
    search_fields = ['cost_center',
                     'equipment',
                     'material__name',
                     'material__item_type__name',
                     'order_type']


@register(LegacyGoodsReceivedNote)
class LegacyGoodsReceivedAdmin(ModelAdmin):
    date_hierarchy = 'transaction_date'
    search_fields = ['invoice_number',
                     'material__name',
                     'material__item_type__name',
                     'purchase_order',
                     'reference_number',
                     'vendor__name']


@register(LegacyItemType)
class LegacyItemTypeAdmin(ModelAdmin):
    search_fields = ['name']


@register(LegacyMaterial)
class LegacyMaterialTypeAdmin(ModelAdmin):
    search_fields = ['name', 'description']


@register(LegacyVendor)
class LegacyVendorAdmin(ModelAdmin):
    search_fields = ['name']
