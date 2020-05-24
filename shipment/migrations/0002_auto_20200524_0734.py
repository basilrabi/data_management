# Generated by Django 3.0.3 on 2020-05-23 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipment', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='laydaysdetail',
            constraint=models.UniqueConstraint(fields=('laydays', 'interval_from'), name='unique_vessel_trip_timestamp'),
        ),
        migrations.AddConstraint(
            model_name='tripdetail',
            constraint=models.UniqueConstraint(fields=('trip', 'interval_from'), name='unique_lct_trip_timestamp'),
        ),
    ]
