# Generated by Django 4.0 on 2022-04-20 05:26

import custom.fields
from django.db import migrations
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0002_equipmentclass_equipmentmanufacturer_equipmentmodel_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipment',
            options={'ordering': [django.db.models.expressions.OrderBy(django.db.models.expressions.F('owner__name')), django.db.models.expressions.OrderBy(django.db.models.expressions.F('model__equipment_class__name')), django.db.models.expressions.OrderBy(django.db.models.expressions.F('fleet_number'))]},
        ),
        migrations.AlterField(
            model_name='equipment',
            name='serial_number',
            field=custom.fields.NameField(blank=True, max_length=100, null=True),
        ),
    ]
