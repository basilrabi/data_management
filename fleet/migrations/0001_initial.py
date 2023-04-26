# Generated by Django 4.2 on 2023-04-26 03:29

import custom.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BodyType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', custom.fields.NameField(max_length=40, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': [models.OrderBy(models.F('name'))],
            },
        ),
        migrations.CreateModel(
            name='EquipmentClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', custom.fields.NameField(max_length=40, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Equipment Class',
                'verbose_name_plural': 'Equipment Classes',
                'ordering': [models.OrderBy(models.F('name'))],
            },
        ),
        migrations.CreateModel(
            name='EquipmentManufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', custom.fields.NameField(max_length=40, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': [models.OrderBy(models.F('name'))],
            },
        ),
        migrations.CreateModel(
            name='TrackedExcavator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fleet_number', models.PositiveSmallIntegerField(unique=True)),
            ],
            options={
                'ordering': ['fleet_number'],
            },
        ),
        migrations.CreateModel(
            name='EquipmentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('name', custom.fields.NameField(max_length=40)),
                ('equipment_class', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fleet.equipmentclass')),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fleet.equipmentmanufacturer')),
            ],
            options={
                'ordering': [models.OrderBy(models.F('manufacturer__name')), models.OrderBy(models.F('equipment_class__name')), models.OrderBy(models.F('name'))],
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acquisition_cost', models.DecimalField(decimal_places=2, default=0, help_text='Cost in Philippine Peso', max_digits=12)),
                ('date_acquired', models.DateField(blank=True, null=True)),
                ('date_phased_out', models.DateField(blank=True, null=True)),
                ('date_disposal', models.DateField(blank=True, null=True)),
                ('asset_tag_id', custom.fields.NameField(blank=True, max_length=20, null=True)),
                ('asset_serial_number', custom.fields.NameField(blank=True, max_length=20, null=True)),
                ('asset_code', custom.fields.NameField(blank=True, help_text='SAP ID', max_length=20, null=True)),
                ('service_life', models.PositiveSmallIntegerField(blank=True, help_text='No. of months', null=True)),
                ('description', models.TextField(blank=True, max_length=50, null=True)),
                ('active', models.BooleanField(default=True)),
                ('fleet_number', models.PositiveSmallIntegerField()),
                ('year_model', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('certificate_of_registration_no', models.CharField(blank=True, max_length=30, null=True)),
                ('cr_date', models.DateField(blank=True, null=True)),
                ('mv_file_no', models.CharField(blank=True, max_length=30, null=True)),
                ('engine_serial_number', custom.fields.AlphaNumeric(blank=True, max_length=100, null=True)),
                ('plate_number', custom.fields.NameField(blank=True, max_length=20, null=True)),
                ('month_of_registration', models.CharField(blank=True, choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], help_text='Based on plate number', max_length=20, null=True)),
                ('chassis_serial_number', custom.fields.NameField(blank=True, max_length=100, null=True)),
                ('body_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='fleet.bodytype')),
                ('department_assigned', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization.organizationunit')),
                ('equipment_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='fleet.equipmentclass')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fleet.equipmentmodel')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organization.organization')),
            ],
            options={
                'verbose_name': 'Equipment',
                'verbose_name_plural': 'Equipment',
                'ordering': [models.OrderBy(models.F('owner__name')), models.OrderBy(models.F('equipment_class__name')), models.OrderBy(models.F('fleet_number'))],
            },
        ),
        migrations.CreateModel(
            name='AdditionalEquipmentCost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acquisition_cost', models.DecimalField(decimal_places=2, default=0, help_text='Cost in Philippine Peso', max_digits=12)),
                ('date_acquired', models.DateField(blank=True, null=True)),
                ('date_phased_out', models.DateField(blank=True, null=True)),
                ('date_disposal', models.DateField(blank=True, null=True)),
                ('asset_tag_id', custom.fields.NameField(blank=True, max_length=20, null=True)),
                ('asset_serial_number', custom.fields.NameField(blank=True, max_length=20, null=True)),
                ('asset_code', custom.fields.NameField(blank=True, help_text='SAP ID', max_length=20, null=True)),
                ('service_life', models.PositiveSmallIntegerField(blank=True, help_text='No. of months', null=True)),
                ('description', models.TextField(blank=True, max_length=50, null=True)),
                ('active', models.BooleanField(default=True)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fleet.equipment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='equipmentmodel',
            constraint=models.UniqueConstraint(fields=('name', 'equipment_class', 'manufacturer'), name='unique_equipment_model_constraint'),
        ),
        migrations.AddConstraint(
            model_name='equipment',
            constraint=models.UniqueConstraint(fields=('fleet_number', 'equipment_class', 'owner'), name='unique_equipment_constraint'),
        ),
    ]
