# Generated by Django 3.0.7 on 2020-08-01 08:28

import custom.fields
import datetime
from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', custom.fields.NameField(max_length=20, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', custom.fields.NameField(max_length=20, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LayDaysDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interval_from', models.DateTimeField()),
                ('laytime_rate', models.PositiveSmallIntegerField(choices=[(100, '100'), (75, '75'), (50, '50'), (25, '25'), (0, '0')])),
                ('interval_class', models.CharField(choices=[('continuous loading', 'Continuous Loading'), ('sun drying', 'Sun Drying'), ('heavy swell', 'Heavy Swell'), ('rain', 'Rain'), ('rain and heavy swell', 'Rain and Heavy Swell'), ('waiting for cargo', 'Waiting for Cargo'), ('waiting for cargo due to rejection', 'Waiting for Cargo (rejected)'), ('waiting for loading commencement', 'Waiting for Loading Commencement'), ('end', 'End'), ('vessel arrived behind of schedule', 'Vessel Arrived Behind of Schedule'), ('others', '-')], max_length=50)),
                ('remarks', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['interval_from'],
            },
        ),
        migrations.CreateModel(
            name='LayDaysDetailComputed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interval_from', models.DateTimeField()),
                ('laytime_rate', models.PositiveSmallIntegerField(help_text='Percent available vessel grabs.')),
                ('time_remaining', models.DurationField()),
                ('interval_class', models.CharField(max_length=50)),
                ('remarks', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['interval_from'],
            },
        ),
        migrations.CreateModel(
            name='LayDaysStatement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vessel_voyage', models.PositiveSmallIntegerField(default=0)),
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
                ('pre_loading_can_test', models.BooleanField(default=False, help_text='Is can test conducted before commencement of loading?', verbose_name='Pre-loading Can Test')),
                ('can_test_factor', models.DecimalField(choices=[(1, '1.0'), (0.5, '0.5'), (0, '0.0')], decimal_places=1, default=0.5, help_text='The number of can tests times this factor times 5 minutes\n            will be deducted to laytime consumed.', max_digits=2)),
                ('time_allowed', models.DurationField(default=datetime.timedelta(0))),
                ('additional_laytime', models.DurationField(default=datetime.timedelta(0))),
                ('demurrage', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('despatch', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('date_saved', models.DateTimeField(blank=True, null=True)),
                ('report_date', models.DateField(blank=True, help_text='Date of statement. Defaults to date_saved.', null=True)),
                ('revised', models.BooleanField(default=False, help_text='This lay days statement is revised from a previous version.')),
                ('date_computed', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': [django.db.models.expressions.OrderBy(django.db.models.expressions.F('completed_loading'), descending=True, nulls_last=False), django.db.models.expressions.OrderBy(django.db.models.expressions.F('arrival_tmc'), descending=True, nulls_last=False)],
            },
        ),
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
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', custom.fields.NameField(max_length=20, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('moisture', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True, verbose_name='%H₂O')),
                ('ni', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True, verbose_name='%Ni')),
                ('fe', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True, verbose_name='%Fe')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
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
                ('continuous', models.BooleanField(default=False, help_text="A continuous trip meets the following conditions: 1) its `interval from` time stamp is equal to its previous trip's `interval to` time stamp and 2) its `interval to` time stamp is equal to the its next trip's `interval from` time stamps.")),
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
                ('spec_tonnage', models.PositiveIntegerField(blank=True, help_text='Tonnage in sales contract.', null=True)),
                ('spec_moisture', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='%H₂O Spec')),
                ('spec_ni', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='%Ni Spec')),
                ('spec_fe', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='%Fe Spec')),
                ('target_tonnage', models.PositiveIntegerField(blank=True, help_text='Determined during initial draft survey.', null=True)),
                ('dump_truck_trips', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('final_ni', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True, verbose_name='%Ni')),
                ('final_fe', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True, verbose_name='%Fe')),
                ('final_moisture', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True, verbose_name='%H₂O')),
                ('base_price', models.DecimalField(blank=True, decimal_places=2, help_text='US$', max_digits=5, null=True)),
                ('final_price', models.DecimalField(blank=True, decimal_places=2, help_text='US$', max_digits=5, null=True)),
                ('boulders_tonnage', models.PositiveIntegerField(blank=True, null=True)),
                ('boulders_processing_cost', models.DecimalField(blank=True, decimal_places=2, help_text='US$', max_digits=8, null=True)),
                ('boulders_freight_cost', models.DecimalField(blank=True, decimal_places=2, help_text='US$', max_digits=8, null=True)),
                ('demurrage', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0'))])),
                ('despatch', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0'))])),
                ('remarks', models.TextField(blank=True, null=True)),
                ('buyer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shipment.Buyer')),
                ('destination', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shipment.Destination')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shipment.Product')),
                ('vessel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shipment.Vessel')),
            ],
            options={
                'ordering': [django.db.models.expressions.OrderBy(django.db.models.expressions.F('laydaysstatement__completed_loading'), descending=True, nulls_last=False), django.db.models.expressions.OrderBy(django.db.models.expressions.F('laydaysstatement__arrival_tmc'), descending=True, nulls_last=False)],
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
        migrations.AddIndex(
            model_name='lct',
            index=models.Index(fields=['name'], name='shipment_lc_name_fd32e7_idx'),
        ),
        migrations.AddField(
            model_name='laydaysstatement',
            name='shipment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shipment.Shipment'),
        ),
        migrations.AddField(
            model_name='laydaysdetailcomputed',
            name='laydays',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shipment.LayDaysStatement'),
        ),
        migrations.AddField(
            model_name='laydaysdetail',
            name='laydays',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shipment.LayDaysStatement'),
        ),
        migrations.AddConstraint(
            model_name='tripdetail',
            constraint=models.UniqueConstraint(fields=('trip', 'interval_from'), name='unique_lct_trip_timestamp'),
        ),
        migrations.AddIndex(
            model_name='shipment',
            index=models.Index(fields=['name'], name='shipment_sh_name_1fb9b5_idx'),
        ),
        migrations.AddConstraint(
            model_name='shipment',
            constraint=models.CheckConstraint(check=models.Q(('demurrage', 0), ('despatch', 0), _connector='OR'), name='dem_des_with_zero'),
        ),
        migrations.AddConstraint(
            model_name='laydaysdetail',
            constraint=models.UniqueConstraint(fields=('laydays', 'interval_from'), name='unique_vessel_trip_timestamp'),
        ),
    ]
