# Generated by Django 4.1.7 on 2023-03-21 08:01

import custom.fields
from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fleet', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shipment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Anchorage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anchored', models.DateTimeField()),
                ('latitude_degree', models.PositiveSmallIntegerField(default=9)),
                ('latitude_minutes', models.DecimalField(decimal_places=5, max_digits=7)),
                ('longitude_degree', models.PositiveSmallIntegerField(default=125)),
                ('longitude_minutes', models.DecimalField(decimal_places=5, max_digits=7)),
                ('geom', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
            ],
            options={
                'ordering': ['anchored'],
            },
        ),
        migrations.CreateModel(
            name='ClippedCluster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_scheduled', models.DateField(blank=True, help_text='Date when the cluster is to be excavated.\n        When this date is set, the geometry cannot be changed.', null=True)),
                ('excavated', models.BooleanField(default=False)),
                ('latest_layout_date', models.DateField(blank=True, help_text='Latest date when the cluster is laid out on the field.\n        This field is auto-generated based on ClusterLayout.', null=True)),
                ('mine_block', models.CharField(blank=True, max_length=20, null=True)),
                ('modified', models.DateTimeField()),
                ('name', models.CharField(max_length=30)),
                ('ore_class', models.CharField(blank=True, max_length=1, null=True)),
                ('z', models.SmallIntegerField(default=0)),
                ('co', models.FloatField(default=0)),
                ('fe', models.FloatField(default=0)),
                ('ni', models.FloatField(default=0)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=3125)),
            ],
        ),
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_scheduled', models.DateField(blank=True, help_text='Date when the cluster is to be excavated.\n        When this date is set, the geometry cannot be changed.', null=True)),
                ('excavated', models.BooleanField(default=False)),
                ('latest_layout_date', models.DateField(blank=True, help_text='Latest date when the cluster is laid out on the field.\n        This field is auto-generated based on ClusterLayout.', null=True)),
                ('mine_block', models.CharField(blank=True, max_length=20, null=True)),
                ('modified', models.DateTimeField()),
                ('name', models.CharField(max_length=30)),
                ('ore_class', models.CharField(blank=True, max_length=1, null=True)),
                ('z', models.SmallIntegerField(default=0)),
                ('co', models.FloatField(default=0)),
                ('fe', models.FloatField(default=0)),
                ('ni', models.FloatField(default=0)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=3125)),
                ('count', models.IntegerField(blank=True, help_text='A unique number for the cluster at the same grade classification and at the same mine block.', null=True)),
                ('distance_from_road', models.FloatField(default=0)),
                ('excavation_rate', models.IntegerField(blank=True, help_text='Percentage of blocks excavated.', null=True)),
                ('exposure_rate', models.IntegerField(blank=True, help_text='Percentage of blocks either exposed or excavated.', null=True)),
            ],
            options={
                'ordering': ['ore_class', 'count'],
            },
        ),
        migrations.CreateModel(
            name='ClusterLayout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('layout_date', models.DateField(help_text='Date when the cluster is laid out on the field. This date\n        cannot be filled out when the date scheduled is still empty.')),
            ],
        ),
        migrations.CreateModel(
            name='Crest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('z', models.PositiveSmallIntegerField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=3125)),
            ],
        ),
        migrations.CreateModel(
            name='DrillHole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
            name='EquipmentLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', custom.fields.NameField(max_length=40, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=3125)),
            ],
            options={
                'verbose_name_plural': 'Facilities',
            },
        ),
        migrations.CreateModel(
            name='FacilityClassification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', custom.fields.NameField(max_length=40, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FLA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', custom.fields.NameField(max_length=40, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=3125)),
            ],
            options={
                'verbose_name': 'Foreshore Lease Agreeement',
            },
        ),
        migrations.CreateModel(
            name='MineBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', custom.fields.MineBlockField(max_length=20, unique=True)),
                ('ridge', models.CharField(choices=[('HY', 'Hayanggabon'), ('T1', 'Taga 1'), ('T2', 'Taga 2'), ('T3', 'Taga 3'), ('UR', 'Urbiztondo'), ('KB', 'Kinalablaban')], max_length=2)),
                ('geom', django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=3125)),
            ],
            options={
                'ordering': ['ridge', 'name'],
            },
        ),
        migrations.CreateModel(
            name='MPSA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', custom.fields.NameField(max_length=40, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=3125)),
            ],
            options={
                'verbose_name': 'Mineral Production Sharing Agreement',
            },
        ),
        migrations.CreateModel(
            name='PEZA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', custom.fields.NameField(max_length=40, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=3125)),
            ],
            options={
                'verbose_name': 'Philippine Economic Zone Authority Area',
            },
        ),
        migrations.CreateModel(
            name='RoadArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_surveyed', models.DateField(unique=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=3125)),
            ],
        ),
        migrations.CreateModel(
            name='Slice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('z', models.IntegerField(help_text='Target elevation of the slice.')),
                ('layer', models.IntegerField(help_text='String id.\n        2: Crest Line (closed line string)\n        7: Road\n        8: Toe Line')),
                ('geom', django.contrib.gis.db.models.fields.LineStringField(dim=3, srid=3125)),
            ],
        ),
        migrations.CreateModel(
            name='Stockpile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', custom.fields.NameField(max_length=100, unique=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=3125)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='WaterBody',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', custom.fields.NameField(max_length=40, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=3125)),
            ],
            options={
                'verbose_name_plural': 'Water Bodies',
            },
        ),
        migrations.AddIndex(
            model_name='slice',
            index=models.Index(fields=['z'], name='location_sl_z_e7f3e5_idx'),
        ),
        migrations.AddConstraint(
            model_name='slice',
            constraint=models.CheckConstraint(check=models.Q(('layer__in', [2, 7, 8])), name='valid_layer'),
        ),
        migrations.AddIndex(
            model_name='roadarea',
            index=models.Index(fields=['date_surveyed'], name='location_ro_date_su_e4d5d6_idx'),
        ),
        migrations.AddField(
            model_name='facility',
            name='classification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='location.facilityclassification'),
        ),
        migrations.AddField(
            model_name='equipmentlocation',
            name='equipment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fleet.equipment'),
        ),
        migrations.AddField(
            model_name='equipmentlocation',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='crest',
            name='slice',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='location.slice'),
        ),
        migrations.AddField(
            model_name='clusterlayout',
            name='cluster',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='location.cluster'),
        ),
        migrations.AddField(
            model_name='cluster',
            name='dumping_area',
            field=models.ForeignKey(blank=True, help_text='Assigned dumping area.', null=True, on_delete=django.db.models.deletion.PROTECT, to='location.stockpile'),
        ),
        migrations.AddField(
            model_name='cluster',
            name='road',
            field=models.ForeignKey(blank=True, help_text='Road used to adjust the cluster geometry.', null=True, on_delete=django.db.models.deletion.PROTECT, to='location.roadarea'),
        ),
        migrations.AddField(
            model_name='clippedcluster',
            name='cluster',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='location.cluster'),
        ),
        migrations.AddField(
            model_name='anchorage',
            name='laydays',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shipment.laydaysstatement'),
        ),
        migrations.AddIndex(
            model_name='crest',
            index=models.Index(fields=['z'], name='location_cr_z_9d2780_idx'),
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
            constraint=models.CheckConstraint(check=models.Q(('distance_from_road__gte', 0)), name='non_negative_distance'),
        ),
        migrations.AddConstraint(
            model_name='cluster',
            constraint=models.UniqueConstraint(fields=('count', 'ore_class', 'mine_block'), name='unique_cluster_name'),
        ),
        migrations.AddIndex(
            model_name='clippedcluster',
            index=models.Index(fields=['z'], name='location_cl_z_dfff73_idx'),
        ),
        migrations.AddIndex(
            model_name='clippedcluster',
            index=models.Index(fields=['mine_block', 'z'], name='location_cl_mine_bl_8e2c79_idx'),
        ),
        migrations.AddConstraint(
            model_name='anchorage',
            constraint=models.CheckConstraint(check=models.Q(('latitude_minutes__gte', 0)), name='lat_floor'),
        ),
        migrations.AddConstraint(
            model_name='anchorage',
            constraint=models.CheckConstraint(check=models.Q(('latitude_minutes__lt', 60)), name='lat_ceiling'),
        ),
        migrations.AddConstraint(
            model_name='anchorage',
            constraint=models.CheckConstraint(check=models.Q(('longitude_minutes__gte', 0)), name='lon_floor'),
        ),
        migrations.AddConstraint(
            model_name='anchorage',
            constraint=models.CheckConstraint(check=models.Q(('longitude_minutes__lt', 60)), name='lon_ceiling'),
        ),
    ]
