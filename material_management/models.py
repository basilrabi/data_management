from django.db.models import (
    CharField,
    DateField,
    FloatField,
    ForeignKey,
    Model,
    PROTECT,
    TextField
)

from custom.models import Classification

# Legacy Models refers to data from the old ERP (Lawsown M3)


class LegacyGoodsIssuance(Model):
    order_number = CharField(max_length=10)
    transaction_date = DateField()
    entry_date = DateField()
    order_type = CharField(max_length=10)
    material = ForeignKey('LegacyMaterial', on_delete=PROTECT)
    cost_center = CharField(max_length=8, null=True, blank=True)
    equipment = TextField(null=True, blank=True)
    quantity = FloatField()
    unit_cost = FloatField(null=True, blank=True)
    total_cost = FloatField(null=True, blank=True)

    class Meta:
        ordering = ['transaction_date', 'entry_date', 'order_number']

    def __str__(self):
        return f'{self.transaction_date} - {self.order_number} - {self.material.name}'


class LegacyGoodsReceivedNote(Model):
    reference_number = CharField(max_length=10)
    transaction_date = DateField()
    entry_date = DateField()
    material = ForeignKey('LegacyMaterial', on_delete=PROTECT)
    purchase_order = CharField(max_length=8)
    vendor = ForeignKey('LegacyVendor', on_delete=PROTECT)
    invoice_number = TextField(null=True, blank=True)
    invoice_amount = FloatField(null=True, blank=True)
    quantity = FloatField()
    purchase_order_price = FloatField()
    discount = FloatField(null=True, blank=True)
    net_price = FloatField()
    total_price = FloatField()

    class Meta:
        ordering = ['transaction_date', 'entry_date', 'reference_number']

    def __str__(self):
        return f'{self.transaction_date} - {self.reference_number} - {self.material.name}'


class LegacyItemType(Classification):
    pass


class LegacyMaterial(Classification):
    item_type = ForeignKey('LegacyItemType', on_delete=PROTECT)


class LegacyVendor(Classification):
    pass
