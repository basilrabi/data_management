from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db.models import (
    DecimalField,
    F,
    Model,
    PositiveSmallIntegerField,
    UniqueConstraint
)


class THPALFeed(Model):
    """
    Ore fed to THPAL in a month.
    """
    year = PositiveSmallIntegerField()
    MONTH_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
        (11, '11'),
        (12, '12'),
    )
    month = PositiveSmallIntegerField(choices=MONTH_CHOICES)
    wmt_oversize = DecimalField(
        null=True, blank=True, max_digits=9, decimal_places=2,
        validators=[MinValueValidator(Decimal(0.00))]
    )
    wmt_undersize = DecimalField(
        null=True, blank=True, max_digits=9, decimal_places=2,
        validators=[MinValueValidator(Decimal(0.00))]
    )
    dmt_undersize = DecimalField(
        max_digits=9, decimal_places=2,
        validators=[MinValueValidator(Decimal(0.00))]
    )
    ni_ton = DecimalField(
        max_digits=7, decimal_places=2,
        validators=[MinValueValidator(Decimal(0.00))]
    )
    co_ton = DecimalField(
        max_digits=6, decimal_places=2,
        validators=[MinValueValidator(Decimal(0.00))]
    )
    chromite_ton = DecimalField(
        help_text = 'Chromite sold by THPAL',
        max_digits=7, decimal_places=2,
        validators=[MinValueValidator(Decimal(0.00))]
    )
    scandium_oxalate_kg = DecimalField(
        help_text = 'Scandium Oxalate sold by THPAL',
        max_digits=7, decimal_places=2,
        validators=[MinValueValidator(Decimal(0.00))]
    )
    # revenue_ni
    # revenue_co
    # revenue_chromite
    # revenue_scandium

    class Meta:
        constraints = [UniqueConstraint(fields=['year', 'month'])]
        ordering = [F('year').desc(), F('month').desc()]

    def __str__(self) -> str:
        return f'{self.year:04d}-{self.month:02d}'
