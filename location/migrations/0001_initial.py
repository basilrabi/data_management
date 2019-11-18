# Generated by Django 2.2.7 on 2019-11-18 14:18

import custom.fields
import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MineBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', custom.fields.MineBlockField(max_length=20, unique=True)),
                ('ridge', models.CharField(choices=[('HY', 'Hayanggabon'), ('T1', 'Taga 1'), ('T2', 'Taga 2'), ('T3', 'Taga 3'), ('UZ', 'Urbiztondo'), ('KB', 'Kinalablaban')], max_length=2)),
                ('geom', django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=3125)),
            ],
            options={
                'ordering': ['ridge', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Stockyard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', custom.fields.PileField(max_length=20, unique=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=3125)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
