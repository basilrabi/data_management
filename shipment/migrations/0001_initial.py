# Generated by Django 2.2.7 on 2019-11-30 02:19

import custom.fields
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LCT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', custom.fields.NameField(max_length=50, unique=True)),
                ('capacity', models.PositiveSmallIntegerField(help_text='Capacity in tons')),
            ],
            options={
                'verbose_name': 'LCT',
                'verbose_name_plural': "LCT's",
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('rejected', 'Cargo Rejected by Vessel'), ('loaded', 'Cargo Loaded to Vessel'), ('partial', 'Cargo Partially Loaded to Vessel')], max_length=20)),
                ('dump_truck_trips', models.PositiveSmallIntegerField(default=0)),
                ('vessel_grab', models.PositiveSmallIntegerField(default=0)),
                ('interval_from', models.DateTimeField(blank=True, null=True)),
                ('interval_to', models.DateTimeField(blank=True, null=True)),
                ('valid', models.BooleanField(default=False, help_text='A valid trip coincides with the shipment schedule.')),
                ('continuous', models.BooleanField(default=False, help_text='A continuous trip as its previous or next trip having adjacent time stamps.')),
                ('lct', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shipment.LCT')),
            ],
            options={
                'ordering': ['lct', '-interval_from'],
            },
        ),
        migrations.CreateModel(
            name='Vessel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', custom.fields.MarineVesselName(max_length=50)),
                ('stripped_name', custom.fields.AlphaNumeric(blank=True, max_length=50, null=True, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TripDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interval_from', models.DateTimeField()),
                ('interval_class', models.CharField(choices=[('preparation_loading', 'Preparation for Loading'), ('loading', 'Loading'), ('preparation_departure', 'Preparation for Departure'), ('travel_to_vessel', 'Travel to Vessel'), ('preparation_unloading', 'Preparation for Unloading'), ('unloading', 'Unloading'), ('preparation_castoff', 'Preparation for Castoff'), ('travel_to_wharf', 'Travel to Wharf'), ('waiting_for_cargo', 'Wating for Cargo'), ('waiting_for_dock', 'Waiting for Available Dock'), ('waiting_for_tide', 'Waiting for Safe Water Level'), ('waiting_for_vessel', 'Waiting for Vessel'), ('swell', 'Swell'), ('rain', 'Rain'), ('rain_swell', 'Rain and Swell'), ('refueling', 'Refueling'), ('rewatering', 'Rewatering'), ('end', 'End')], max_length=30)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shipment.Trip')),
            ],
            options={
                'ordering': ['interval_from'],
            },
        ),
        migrations.AddField(
            model_name='trip',
            name='vessel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shipment.Vessel'),
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', custom.fields.NameField(max_length=10, unique=True)),
                ('start_loading', models.DateTimeField()),
                ('end_loading', models.DateTimeField(blank=True, null=True)),
                ('dump_truck_trips', models.PositiveSmallIntegerField(default=0)),
                ('tonnage', models.PositiveIntegerField(default=0)),
                ('vessel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shipment.Vessel')),
            ],
            options={
                'ordering': ['-start_loading', 'name'],
            },
        ),
        migrations.CreateModel(
            name='LCTContract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField()),
                ('end', models.DateField(blank=True, null=True)),
                ('lct', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shipment.LCT')),
            ],
            options={
                'verbose_name': 'LCT Contract',
                'verbose_name_plural': 'LCT Contracts',
                'ordering': ['lct', 'start'],
            },
        ),
        migrations.CreateModel(
            name='LayDaysStatement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vessel_voyage', models.CharField(blank=True, max_length=20, null=True)),
                ('arrival_pilot', models.DateTimeField(blank=True, null=True, verbose_name='Arrival at Surigao Pilot Station')),
                ('arrival_tmc', models.DateTimeField(blank=True, null=True, verbose_name='Arrival at TMC Port')),
                ('nor_tender', models.DateTimeField(blank=True, null=True, verbose_name='Notice of Readiness Tendered')),
                ('nor_accepted', models.DateTimeField(blank=True, null=True, verbose_name='Notice of Readiness Accepted')),
                ('commenced_laytime', models.DateTimeField(blank=True, null=True)),
                ('commenced_loading', models.DateTimeField(blank=True, null=True)),
                ('completed_loading', models.DateTimeField(blank=True, null=True)),
                ('cargo_description', custom.fields.NameField(default='NICKEL ORE', max_length=20)),
                ('tonnage', models.PositiveIntegerField(blank=True, null=True)),
                ('loading_terms', models.PositiveSmallIntegerField(default=6000, help_text='Agreed loading rate (tons per day).')),
                ('demurrage_rate', models.PositiveSmallIntegerField(default=11000, help_text='US Dollar per day')),
                ('despatch_rate', models.PositiveSmallIntegerField(default=5500, help_text='US Dollar per day')),
                ('can_test', models.PositiveSmallIntegerField(default=0, help_text='Number of can tests performed.')),
                ('time_allowed', models.DurationField(default=datetime.timedelta(0))),
                ('time_used', models.DurationField(default=datetime.timedelta(0))),
                ('demurrage', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('despatch', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('shipment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shipment.Shipment')),
            ],
            options={
                'ordering': ['-completed_loading'],
            },
        ),
        migrations.CreateModel(
            name='LayDaysDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interval_from', models.DateTimeField()),
                ('loading_rate', models.PositiveSmallIntegerField(help_text='Percent available vessel grabs.')),
                ('interval_class', models.CharField(choices=[('can_test', 'Can Test'), ('end', 'End'), ('loading', 'Continuous Loading'), ('others', '-'), ('sun_dry', 'Cargo Sun Drying'), ('swell', 'Heavy Swell'), ('rain', 'Rain'), ('rain_swell', 'Rain and Swell'), ('waiting_for_cargo', 'Waiting for Cargo')], max_length=30)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('laydays', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shipment.LayDaysStatement')),
            ],
            options={
                'ordering': ['interval_from'],
            },
        ),
    ]
