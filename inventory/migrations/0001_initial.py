# Generated by Django 3.0.3 on 2020-03-05 06:02

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DrillArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factor', models.DecimalField(blank=True, decimal_places=4, default=1, max_digits=5, null=True)),
                ('influence', django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=3125)),
                ('drill_hole', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='location.DrillHole')),
            ],
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('z', models.SmallIntegerField()),
                ('ni', models.FloatField()),
                ('fe', models.FloatField()),
                ('co', models.FloatField()),
                ('excavated', models.BooleanField(default=False)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=3125)),
                ('cluster', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='location.Cluster')),
            ],
        ),
        migrations.AddConstraint(
            model_name='drillarea',
            constraint=models.CheckConstraint(check=models.Q(factor__lte=1), name='factor_max_drill_aoi'),
        ),
        migrations.AddConstraint(
            model_name='drillarea',
            constraint=models.CheckConstraint(check=models.Q(factor__gte=0), name='factor_min_drill_aoi'),
        ),
        migrations.AddIndex(
            model_name='block',
            index=models.Index(fields=['z', 'ni'], name='inventory_b_z_be93d7_idx'),
        ),
    ]
