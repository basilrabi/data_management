# Generated by Django 3.0.7 on 2020-07-30 07:07

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipment', '0005_auto_20200730_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='demurrage',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='despatch',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0'))]),
        ),
    ]
