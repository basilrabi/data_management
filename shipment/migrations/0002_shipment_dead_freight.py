# Generated by Django 3.1.1 on 2020-10-10 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment',
            name='dead_freight',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='US$', max_digits=8, null=True),
        ),
    ]
