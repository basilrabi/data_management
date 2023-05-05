from django.db.models import (
    CheckConstraint,
    DecimalField,
    F,
    ForeignKey,
    Index,
    Model,
    PositiveIntegerField,
    PositiveSmallIntegerField,
    PROTECT,
    Q,
    SET_NULL,
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

    def __str__(self) -> str:
        return f'{self.old_cost_center} - {self.sap_cost_center}'


class GeneralLedgerAccount(Model):
    """
    GL Account
    """
    code = PositiveIntegerField(unique=True)
    description = TextField()

    class Meta:
        ordering = [F('code').asc()]

    def __str__(self) -> str:
        return self.description


class MonthlyCost(Model):
    """
    Cost provided by finance in pesos.
    """
    year = PositiveSmallIntegerField()
    month = PositiveSmallIntegerField()
    cost_center = ForeignKey('SapCostCenter', on_delete=PROTECT)
    gl = ForeignKey('GeneralLedgerAccount', on_delete=PROTECT)
    budget = DecimalField(
        decimal_places=2, default=0, max_digits=13,
        help_text="Planned prior to the fiscal year."
    )
    adjusted_budget = DecimalField(
        decimal_places=2, default=0, max_digits=13,
        help_text="Approved minor revision of budget. May be updated from time to time."
    )
    forecast = DecimalField(
        decimal_places=2, default=0, max_digits=13,
        help_text="Recomputed cost for the fiscal year due to major changes in operating assumptions."
    )
    actual = DecimalField(
        decimal_places=2, default=0, max_digits=13,
        help_text="Actual booked cost."
    )
    remarks = TextField(blank=True, null=True)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(year__gte=2021), name='monthlycost_year_min'
            ),
            CheckConstraint(
                check=Q(month__gte=1), name='monthlycost_month_min'
            ),
            CheckConstraint(
                check=Q(month__lte=13), name='monthlycost_month_max'
            ),
            UniqueConstraint(
                fields=['year', 'month', 'cost_center', 'gl'],
                name='unique_monthly_cost'
            )
        ]
        indexes = [
            Index(fields=['year', 'month']),
            Index(fields=['month'])
        ]
        ordering = ['-year', '-month', 'cost_center', 'gl']

    def __str__(self) -> str:
        return f'{self.year}-{self.month:02}-{self.cost_center.name}-{self.gl.code}'


class ProfitCenter(Classification):
    """
    Profit center definitions set by NAC.
    """
    pass


class SapCostCenter(Classification):
    """
    Cost center definitions in SAP ERP.
    """
    long_name = TextField(null=True, blank=True)
    remarks = TextField(null=True, blank=True)
    profit_center = ForeignKey(
        'ProfitCenter', on_delete=SET_NULL, null=True, blank=True
    )
