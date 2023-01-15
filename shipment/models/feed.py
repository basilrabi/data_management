from decimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    CheckConstraint,
    DateField,
    DecimalField,
    F,
    FileField,
    FloatField,
    Model,
    PositiveSmallIntegerField,
    Q,
    UniqueConstraint
)

from custom.models import SpaceLess
from custom.variables import MONTH_CHOICES


class ChromiteSale(Model):
    shipment = PositiveSmallIntegerField(primary_key=True)
    provisional_invoice = SpaceLess(max_length=40)
    provisional_invoice_date = DateField(null=True, blank=True)
    provisional_wmt = DecimalField(
        max_digits=9, decimal_places=3,
        validators=[MinValueValidator(Decimal(5000.000))]
    )
    provisional_moisture = DecimalField(
        '%H₂O', max_digits=6, decimal_places=4,
        validators=[
            MaxValueValidator(Decimal(10.0000)),
            MinValueValidator(Decimal(2.0000))
        ]
    )
    provisional_dmt = FloatField(blank=True)
    provisional_chromite_content = DecimalField(
        '%Chromite', max_digits=6, decimal_places=4,
        validators=[
            MaxValueValidator(Decimal(60.0000)),
            MinValueValidator(Decimal(30.0000))
        ]
    )
    provisional_usd_per_dmt = DecimalField(
        '$US/dmt', max_digits=7, decimal_places=3,
        validators=[MinValueValidator(Decimal(100.000))]
    )
    provisional_invoice_rate = DecimalField(
        help_text='Percentage of billed for provisional invoice.',
        default=93, max_digits=5, decimal_places=2,
        validators=[
            MaxValueValidator(Decimal(100.00)),
            MinValueValidator(Decimal(80.00))
        ]
    )
    tmc_share = DecimalField(
        help_text='Revenue share of TMC in percentage.',
        default=4, max_digits=5, decimal_places=2,
        validators=[
            MaxValueValidator(Decimal(40.00)),
            MinValueValidator(Decimal(2.00))
        ]
    )
    provisional_shipment_price_usd = DecimalField(
        max_digits=10, decimal_places=2, blank=True
    )
    provisional_revenue_usd = DecimalField(
        max_digits=9, decimal_places=2, blank=True
    )
    provisional_revenue_php = FloatField(blank=True)
    bill_of_lading_date = DateField()
    usd_to_php = DecimalField(
        max_digits=6, decimal_places=3,
        validators=[MinValueValidator(Decimal(30.000))]
    )
    final_invoice = SpaceLess(max_length=40, null=True, blank=True)
    final_invoice_date = DateField(null=True, blank=True)
    final_wmt = DecimalField(
        max_digits=9, decimal_places=3, null=True, blank=True,
        validators=[MinValueValidator(Decimal(5000.000))]
    )
    final_moisture = DecimalField(
        '%H₂O', max_digits=6, decimal_places=4, null=True, blank=True,
        validators=[
            MaxValueValidator(Decimal(10.0000)),
            MinValueValidator(Decimal(2.0000))
        ]
    )
    final_dmt = FloatField(null=True, blank=True)
    final_chromite_content = DecimalField(
        '%Chromite', max_digits=6, decimal_places=4, null=True, blank=True,
        validators=[
            MaxValueValidator(Decimal(60.0000)),
            MinValueValidator(Decimal(30.0000))
        ]
    )
    final_usd_per_dmt = DecimalField(
        '$US/dmt', max_digits=7, decimal_places=3, null=True, blank=True,
        validators=[MinValueValidator(Decimal(100.000))]
    )
    final_shipment_price_usd = DecimalField(
        help_text='93% of total amount',
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    final_revenue_usd = DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True
    )
    final_revenue_php = DecimalField(
        max_digits=11, decimal_places=2, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        self.provisional_dmt = self.provisional_wmt * ((100 - self.provisional_moisture) / 100)
        self.provisional_shipment_price_usd = round(
            round(
                self.provisional_dmt * self.provisional_usd_per_dmt, 2
            ) * self.provisional_invoice_rate / 100,
            2
        )
        self.provisional_revenue_usd = round(
            self.provisional_shipment_price_usd * self.tmc_share / 100,
            2
        )
        self.provisional_revenue_php = self.provisional_revenue_usd * self.usd_to_php
        if self.final_wmt and self.final_moisture:
            self.final_dmt = self.final_wmt * ((100 - self.final_moisture) / 100)
            if self.final_usd_per_dmt:
                self.final_shipment_price_usd = round(
                    round(
                        self.final_dmt * self.final_usd_per_dmt, 2
                    ) * self.provisional_invoice_rate / 100,
                    2
                )
                self.final_revenue_usd = round(
                    self.final_shipment_price_usd * self.tmc_share / 100,
                    2
                )
        super().save(*args, **kwargs)


class ScandiumSale(Model):
    shipment = PositiveSmallIntegerField(primary_key=True)
    invoice_date = DateField()
    bill_of_lading_date = DateField(null=True, blank=True)
    precipitate_wet_kg = DecimalField(
        help_text = 'Scandium Oxalate Precipitate sold by THPAL in wet kg',
        max_digits=7, decimal_places=2,
        validators=[MinValueValidator(Decimal(1.00))]
    )
    precipitate_dry_kg = DecimalField(
        help_text = 'Scandium Oxalate Precipitate sold by THPAL in dry kg',
        max_digits=7, decimal_places=2,
        validators=[MinValueValidator(Decimal(100.00))]
    )
    scandium_oxalate_percentage = DecimalField(
        '%Scandium Oxalate', max_digits=5, decimal_places=3,
        validators=[
            MaxValueValidator(Decimal(40.000)),
            MinValueValidator(Decimal(10.000))
        ]
    )
    scandium_oxalate_kg = DecimalField(max_digits=5, decimal_places=1)
    scandium_oxide_kg = DecimalField(max_digits=6, decimal_places=1)
    usd_per_kg_scandium_oxide = DecimalField(
        max_digits=7, decimal_places=2
    )

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(scandium_oxide_kg__gt=F('scandium_oxalate_kg') * 1.52),
                name='min_scandium_oxide'
            ),
            CheckConstraint(
                check=Q(scandium_oxide_kg__lt=F('scandium_oxalate_kg') * 1.54),
                name='max_scandium_oxide'
            )
        ]

class THPALFeed(Model):
    """
    Ore fed to THPAL in a month.
    """
    year = PositiveSmallIntegerField()
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
    certificate = FileField(
        upload_to='assay/hpal_feed/', null=True, blank=True
    )

    class Meta:
        constraints = [UniqueConstraint(fields=['year', 'month'])]
        ordering = [F('year').desc(), F('month').desc()]

    def __str__(self) -> str:
        return f'{self.year:04d}-{self.month:02d}'
