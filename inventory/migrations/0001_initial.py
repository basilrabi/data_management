# Generated by Django 3.0.3 on 2020-02-07 09:40

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
                ('cluster', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='location.Cluster')),
            ],
        ),
        migrations.AddIndex(
            model_name='block',
            index=models.Index(fields=['z', 'ni'], name='inventory_b_z_be93d7_idx'),
        ),
    ]
