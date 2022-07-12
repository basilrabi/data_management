from django.db.models import (
    F,
    ForeignKey,
    Model,
    PositiveIntegerField,
    PROTECT,
    TextField,
    UniqueConstraint
)

from custom.models import Classification


class CostCenter(Classification):
    """
    TMC's in-house cost center names.
    """
    pass


class CostCenterConversion(Model):
    """
    Matching between in-house and SAP-ERP cost center naming convention.
    """
    old_cost_center = ForeignKey('CostCenter', on_delete=PROTECT)
    sap_cost_center = ForeignKey('SapCostCenter', on_delete=PROTECT)

    class Meta:
        constraints = [UniqueConstraint(
            fields=['old_cost_center', 'sap_cost_center'],
            name='unique_cost_center_conversion'
        )]
        ordering = [
            F('sap_cost_center__name').asc(),
            F('old_cost_center__name').asc()
        ]


class GeneralLedgerAccount(Model):
    """
    GL Account
    """
    code = PositiveIntegerField(unique=True)
    description = TextField()


class SapCostCenter(Classification):
    """
    Cost center definitions in SAP ERP.
    """
    remarks = TextField(null=True, blank=True)
