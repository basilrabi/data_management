# Generated by Django 3.1.1 on 2020-09-11 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipment', '0005_auto_20200911_1921'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='trip',
            name='unique_lct_trip_interval',
        ),
        migrations.AddConstraint(
            model_name='trip',
            constraint=models.UniqueConstraint(fields=('lct', 'interval_from', 'interval_to'), name='unique_lct_trip_interval'),
        ),
    ]
