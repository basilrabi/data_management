# Generated by Django 3.2.5 on 2021-07-14 18:19

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
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factor', models.DecimalField(blank=True, decimal_places=4, default=1, max_digits=5, null=True)),
                ('influence', django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=3125)),
                ('drill_hole', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='location.drillhole')),
            ],
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('z', models.SmallIntegerField(help_text='Elevation of the top face of the block.')),
                ('ni', models.FloatField(help_text='Estimated nickel content of the block in percent.')),
                ('fe', models.FloatField(help_text='Estimated iron content of the block in percent.')),
                ('co', models.FloatField(help_text='Estimated cobalt content of the block in percent.')),
                ('depth', models.FloatField(blank=True, help_text='Distance of the centroid from the surface. A positive\n        value means that the centroid is still below the surface.\n        ', null=True)),
                ('planned_excavation_date', models.DateField(blank=True, null=True)),
                ('exposed', models.BooleanField(blank=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=3125)),
                ('cluster', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='location.cluster')),
            ],
        ),
        migrations.AddConstraint(
            model_name='drillarea',
            constraint=models.CheckConstraint(check=models.Q(('factor__lte', 1)), name='factor_max_drill_aoi'),
        ),
        migrations.AddConstraint(
            model_name='drillarea',
            constraint=models.CheckConstraint(check=models.Q(('factor__gte', 0)), name='factor_min_drill_aoi'),
        ),
        migrations.AddIndex(
            model_name='block',
            index=models.Index(fields=['z'], name='inventory_b_z_6e1019_idx'),
        ),
        migrations.AddIndex(
            model_name='block',
            index=models.Index(fields=['exposed', 'z', 'planned_excavation_date'], name='inventory_b_exposed_213b67_idx'),
        ),
        migrations.AddIndex(
            model_name='block',
            index=models.Index(fields=['exposed', 'fe', 'ni', 'z', 'planned_excavation_date'], name='inventory_b_exposed_350d62_idx'),
        ),
    ]
