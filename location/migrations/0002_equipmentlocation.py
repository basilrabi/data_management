# Generated by Django 4.0.4 on 2022-04-29 01:37

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0002_equipment_unique_equipment_constraint'),
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquipmentLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fleet.equipment')),
            ],
        ),
    ]
