# Generated by Django 3.1 on 2020-08-14 00:42

import custom.fields
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('z', models.SmallIntegerField(default=0)),
                ('count', models.IntegerField(blank=True, help_text='A unique number for the cluster at the same grade classification and at the same mine block.', null=True)),
                ('ore_class', models.CharField(blank=True, max_length=1, null=True)),
                ('mine_block', models.CharField(blank=True, max_length=20, null=True)),
                ('ni', models.FloatField(default=0)),
                ('fe', models.FloatField(default=0)),
                ('co', models.FloatField(default=0)),
                ('distance_from_road', models.FloatField(default=0)),
                ('date_scheduled', models.DateField(blank=True, help_text='Date when the cluster geometry is finalized. When this\n        date is set, the geometry cannot be changed.', null=True)),
                ('layout_date', models.DateField(blank=True, help_text='Date when the cluster is laid out on the field. When this\n        date is set, the date scheduled cannot be changed. This date cannot be\n        filled out when the date scheduled is still empty.', null=True)),
                ('excavated', models.BooleanField(default=False)),
                ('modified', models.DateTimeField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=3125)),
            ],
            options={
                'ordering': ['ore_class', 'count'],
            },
        ),
        migrations.CreateModel(
            name='DrillHole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', custom.fields.NameField(max_length=20, unique=True)),
                ('date_drilled', models.DateField(blank=True, null=True)),
                ('local_block', models.CharField(blank=True, help_text='block location in local coordinates', max_length=20, null=True)),
                ('local_easting', models.CharField(blank=True, help_text='collar x-coordinates in local grid', max_length=20, null=True)),
                ('local_northing', models.CharField(blank=True, help_text='collar y-coordinates in local grid', max_length=20, null=True)),
                ('local_z', models.FloatField(blank=True, help_text='collar elevation prior to the use of SRID:3125', null=True)),
                ('x', models.FloatField(blank=True, help_text='collar x-coordinates in SRID:3125', null=True)),
                ('y', models.FloatField(blank=True, help_text='collar y-coordinates in SRID:3125', null=True)),
                ('z', models.FloatField(blank=True, help_text='collar elevation', null=True)),
                ('z_present', models.FloatField(blank=True, help_text='present ground elevation', null=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=3125)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MineBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', custom.fields.MineBlockField(max_length=20, unique=True)),
                ('ridge', models.CharField(choices=[('HY', 'Hayanggabon'), ('T1', 'Taga 1'), ('T2', 'Taga 2'), ('T3', 'Taga 3'), ('UR', 'Urbiztondo'), ('KB', 'Kinalablaban')], max_length=2)),
                ('geom', django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=3125)),
            ],
            options={
                'ordering': ['ridge', 'name'],
            },
        ),
        migrations.CreateModel(
            name='RoadArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_surveyed', models.DateField(unique=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=3125)),
            ],
        ),
        migrations.CreateModel(
            name='Slice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('z', models.IntegerField(help_text='Target elevation of the slice.')),
                ('layer', models.IntegerField(help_text='String id.\n        2: Crest Line (closed line string)\n        7: Road\n        8: Toe Line')),
                ('geom', django.contrib.gis.db.models.fields.LineStringField(dim=3, srid=3125)),
            ],
        ),
        migrations.CreateModel(
            name='Stockpile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', custom.fields.PileField(max_length=20, unique=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=3125)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddIndex(
            model_name='slice',
            index=models.Index(fields=['z'], name='location_sl_z_e7f3e5_idx'),
        ),
        migrations.AddConstraint(
            model_name='slice',
            constraint=models.CheckConstraint(check=models.Q(layer__in=[2, 7, 8]), name='valid_layer'),
        ),
        migrations.AddIndex(
            model_name='roadarea',
            index=models.Index(fields=['date_surveyed'], name='location_ro_date_su_e4d5d6_idx'),
        ),
        migrations.AddField(
            model_name='cluster',
            name='road',
            field=models.ForeignKey(blank=True, help_text='Road used to adjust the cluster geometry.', null=True, on_delete=django.db.models.deletion.PROTECT, to='location.roadarea'),
        ),
        migrations.AddIndex(
            model_name='cluster',
            index=models.Index(fields=['z'], name='location_cl_z_0cb9f0_idx'),
        ),
        migrations.AddIndex(
            model_name='cluster',
            index=models.Index(fields=['mine_block', 'z'], name='location_cl_mine_bl_630a61_idx'),
        ),
        migrations.AddConstraint(
            model_name='cluster',
            constraint=models.CheckConstraint(check=models.Q(distance_from_road__gte=0), name='non_negative_distance'),
        ),
        migrations.AddConstraint(
            model_name='cluster',
            constraint=models.UniqueConstraint(fields=('count', 'ore_class', 'mine_block'), name='unique_cluster_name'),
        ),
    ]
