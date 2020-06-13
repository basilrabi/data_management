# Generated by Django 3.0.6 on 2020-06-09 11:11

import custom.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fleet', '0001_initial'),
        ('location', '0001_initial'),
        ('personnel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lithology',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', custom.fields.SpaceLess(max_length=10, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MiningSample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_received_for_preparation', models.DateField(blank=True, null=True)),
                ('date_prepared', models.DateField(blank=True, null=True)),
                ('date_received_for_analysis', models.DateField(blank=True, null=True)),
                ('date_analyzed', models.DateField(blank=True, null=True)),
                ('al', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True, verbose_name='%Al')),
                ('c', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True, verbose_name='%C')),
                ('co', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True, verbose_name='%Co')),
                ('cr', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True, verbose_name='%Cr')),
                ('fe', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True, verbose_name='%Fe')),
                ('mg', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True, verbose_name='%Mg')),
                ('ni', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True, verbose_name='%Ni')),
                ('sc', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True, verbose_name='%Sc')),
                ('si', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True, verbose_name='%Si')),
                ('moisture', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True, verbose_name='%H₂O')),
                ('series_number', models.PositiveSmallIntegerField()),
                ('material', models.CharField(blank=True, max_length=1, null=True)),
                ('ridge', models.CharField(blank=True, max_length=2, null=True)),
                ('start_collection', models.DateField(blank=True, null=True)),
                ('month', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('end_collection', models.DateField(blank=True, null=True)),
                ('trips', models.PositiveSmallIntegerField(default=0)),
                ('ready_for_delivery', models.BooleanField(default=False)),
                ('dumping_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.Stockyard')),
            ],
            options={
                'ordering': ['-start_collection__year', '-month', '-series_number'],
            },
        ),
        migrations.CreateModel(
            name='PilingMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', custom.fields.NameField(max_length=20, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TripsPerPile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('effectivity', models.DateField()),
                ('end', models.DateField(blank=True, null=True)),
                ('trips', models.PositiveSmallIntegerField()),
                ('piling_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sampling.PilingMethod')),
            ],
            options={
                'ordering': ['-effectivity'],
            },
        ),
        migrations.CreateModel(
            name='MiningSampleReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('shift_collected', models.CharField(choices=[('D', 'Day'), ('N', 'Night'), ('M', 'M')], max_length=1)),
                ('dumping_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.Stockyard')),
                ('foreman', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managedminingsamplereport', to='personnel.Person')),
                ('piling_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sampling.PilingMethod')),
                ('sampler', models.ManyToManyField(blank=True, related_name='samplereport', to='personnel.Person')),
                ('source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='location.Cluster')),
                ('supervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supervisedminingsamplereport', to='personnel.Person')),
                ('tx', models.ManyToManyField(to='fleet.TrackedExcavator', verbose_name='TX')),
            ],
            options={
                'ordering': ['-date', '-shift_collected'],
            },
        ),
        migrations.CreateModel(
            name='MiningSampleIncrement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trips', models.PositiveSmallIntegerField()),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sampling.MiningSampleReport')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sampling.MiningSample')),
            ],
            options={
                'ordering': ['sample__series_number'],
            },
        ),
        migrations.AddField(
            model_name='miningsample',
            name='piling_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sampling.PilingMethod'),
        ),
        migrations.CreateModel(
            name='DrillCoreSample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_received_for_preparation', models.DateField(blank=True, null=True)),
                ('date_prepared', models.DateField(blank=True, null=True)),
                ('date_received_for_analysis', models.DateField(blank=True, null=True)),
                ('date_analyzed', models.DateField(blank=True, null=True)),
                ('al', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True, verbose_name='%Al')),
                ('c', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True, verbose_name='%C')),
                ('co', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True, verbose_name='%Co')),
                ('cr', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True, verbose_name='%Cr')),
                ('fe', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True, verbose_name='%Fe')),
                ('mg', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True, verbose_name='%Mg')),
                ('ni', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True, verbose_name='%Ni')),
                ('sc', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True, verbose_name='%Sc')),
                ('si', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True, verbose_name='%Si')),
                ('moisture', models.DecimalField(blank=True, decimal_places=4, max_digits=6, null=True, verbose_name='%H₂O')),
                ('interval_from', models.DecimalField(decimal_places=3, max_digits=5)),
                ('interval_to', models.DecimalField(decimal_places=3, max_digits=5)),
                ('description', models.TextField(blank=True, null=True)),
                ('excavated_date', models.DateField(blank=True, null=True)),
                ('drill_hole', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.DrillHole')),
                ('lithology', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sampling.Lithology')),
            ],
            options={
                'ordering': ['interval_from'],
            },
        ),
        migrations.CreateModel(
            name='AcquiredMiningSample',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('sampling.miningsample',),
        ),
        migrations.CreateModel(
            name='DrillCore',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('sampling.drillcoresample',),
        ),
        migrations.CreateModel(
            name='DrillCoreAssay',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('sampling.drillcoresample',),
        ),
        migrations.CreateModel(
            name='MiningSampleAssay',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('sampling.miningsample',),
        ),
        migrations.AddConstraint(
            model_name='tripsperpile',
            constraint=models.CheckConstraint(check=models.Q(trips__gt=0), name='trips_min_1'),
        ),
        migrations.AddConstraint(
            model_name='miningsampleincrement',
            constraint=models.UniqueConstraint(fields=('sample', 'report'), name='sample_increment_report_constraint'),
        ),
        migrations.AddConstraint(
            model_name='miningsample',
            constraint=models.UniqueConstraint(fields=('ridge', 'material', 'month', 'series_number'), name='mining_sample_constraint'),
        ),
        migrations.AddConstraint(
            model_name='miningsample',
            constraint=models.CheckConstraint(check=models.Q(al__lte=100), name='al_max_100_miningsample'),
        ),
        migrations.AddConstraint(
            model_name='miningsample',
            constraint=models.CheckConstraint(check=models.Q(c__lte=100), name='c_max_100_miningsample'),
        ),
        migrations.AddConstraint(
            model_name='miningsample',
            constraint=models.CheckConstraint(check=models.Q(co__lte=100), name='co_max_100_miningsample'),
        ),
        migrations.AddConstraint(
            model_name='miningsample',
            constraint=models.CheckConstraint(check=models.Q(cr__lte=100), name='cr_max_100_miningsample'),
        ),
        migrations.AddConstraint(
            model_name='miningsample',
            constraint=models.CheckConstraint(check=models.Q(fe__lte=100), name='fe_max_100_miningsample'),
        ),
        migrations.AddConstraint(
            model_name='miningsample',
            constraint=models.CheckConstraint(check=models.Q(mg__lte=100), name='mg_max_100_miningsample'),
        ),
        migrations.AddConstraint(
            model_name='miningsample',
            constraint=models.CheckConstraint(check=models.Q(ni__lte=100), name='ni_max_100_miningsample'),
        ),
        migrations.AddConstraint(
            model_name='miningsample',
            constraint=models.CheckConstraint(check=models.Q(sc__lte=100), name='sc_max_100_miningsample'),
        ),
        migrations.AddConstraint(
            model_name='miningsample',
            constraint=models.CheckConstraint(check=models.Q(si__lte=100), name='si_max_100_miningsample'),
        ),
        migrations.AddConstraint(
            model_name='miningsample',
            constraint=models.CheckConstraint(check=models.Q(moisture__lte=100), name='moisture_max_100_miningsample'),
        ),
        migrations.AddConstraint(
            model_name='miningsample',
            constraint=models.CheckConstraint(check=models.Q(al__gte=0), name='al_min_0_miningsample'),
        ),
        migrations.AddConstraint(
            model_name='miningsample',
            constraint=models.CheckConstraint(check=models.Q(c__gte=0), name='c_min_0_miningsample'),
        ),
        migrations.AddConstraint(
            model_name='miningsample',
            constraint=models.CheckConstraint(check=models.Q(co__gte=0), name='co_min_0_miningsample'),
        ),
        migrations.AddConstraint(
            model_name='miningsample',
            constraint=models.CheckConstraint(check=models.Q(cr__gte=0), name='cr_min_0_miningsample'),
        ),
        migrations.AddConstraint(
            model_name='miningsample',
            constraint=models.CheckConstraint(check=models.Q(fe__gte=0), name='fe_min_0_miningsample'),
        ),
        migrations.AddConstraint(
            model_name='miningsample',
            constraint=models.CheckConstraint(check=models.Q(mg__gte=0), name='mg_min_0_miningsample'),
        ),
        migrations.AddConstraint(
            model_name='miningsample',
            constraint=models.CheckConstraint(check=models.Q(ni__gte=0), name='ni_min_0_miningsample'),
        ),
        migrations.AddConstraint(
            model_name='miningsample',
            constraint=models.CheckConstraint(check=models.Q(sc__gte=0), name='sc_min_0_miningsample'),
        ),
        migrations.AddConstraint(
            model_name='miningsample',
            constraint=models.CheckConstraint(check=models.Q(si__gte=0), name='si_min_0_miningsample'),
        ),
        migrations.AddConstraint(
            model_name='miningsample',
            constraint=models.CheckConstraint(check=models.Q(moisture__gte=0), name='moisture_min_0_miningsample'),
        ),
        migrations.AddConstraint(
            model_name='drillcoresample',
            constraint=models.CheckConstraint(check=models.Q(al__lte=100), name='al_max_100_drillcore'),
        ),
        migrations.AddConstraint(
            model_name='drillcoresample',
            constraint=models.CheckConstraint(check=models.Q(c__lte=100), name='c_max_100_drillcore'),
        ),
        migrations.AddConstraint(
            model_name='drillcoresample',
            constraint=models.CheckConstraint(check=models.Q(co__lte=100), name='co_max_100_drillcore'),
        ),
        migrations.AddConstraint(
            model_name='drillcoresample',
            constraint=models.CheckConstraint(check=models.Q(cr__lte=100), name='cr_max_100_drillcore'),
        ),
        migrations.AddConstraint(
            model_name='drillcoresample',
            constraint=models.CheckConstraint(check=models.Q(fe__lte=100), name='fe_max_100_drillcore'),
        ),
        migrations.AddConstraint(
            model_name='drillcoresample',
            constraint=models.CheckConstraint(check=models.Q(mg__lte=100), name='mg_max_100_drillcore'),
        ),
        migrations.AddConstraint(
            model_name='drillcoresample',
            constraint=models.CheckConstraint(check=models.Q(ni__lte=100), name='ni_max_100_drillcore'),
        ),
        migrations.AddConstraint(
            model_name='drillcoresample',
            constraint=models.CheckConstraint(check=models.Q(sc__lte=100), name='sc_max_100_drillcore'),
        ),
        migrations.AddConstraint(
            model_name='drillcoresample',
            constraint=models.CheckConstraint(check=models.Q(si__lte=100), name='si_max_100_drillcore'),
        ),
        migrations.AddConstraint(
            model_name='drillcoresample',
            constraint=models.CheckConstraint(check=models.Q(moisture__lte=100), name='moisture_max_100_drillcore'),
        ),
        migrations.AddConstraint(
            model_name='drillcoresample',
            constraint=models.CheckConstraint(check=models.Q(al__gte=0), name='al_min_0_drillcore'),
        ),
        migrations.AddConstraint(
            model_name='drillcoresample',
            constraint=models.CheckConstraint(check=models.Q(c__gte=0), name='c_min_0_drillcore'),
        ),
        migrations.AddConstraint(
            model_name='drillcoresample',
            constraint=models.CheckConstraint(check=models.Q(co__gte=0), name='co_min_0_drillcore'),
        ),
        migrations.AddConstraint(
            model_name='drillcoresample',
            constraint=models.CheckConstraint(check=models.Q(cr__gte=0), name='cr_min_0_drillcore'),
        ),
        migrations.AddConstraint(
            model_name='drillcoresample',
            constraint=models.CheckConstraint(check=models.Q(fe__gte=0), name='fe_min_0_drillcore'),
        ),
        migrations.AddConstraint(
            model_name='drillcoresample',
            constraint=models.CheckConstraint(check=models.Q(mg__gte=0), name='mg_min_0_drillcore'),
        ),
        migrations.AddConstraint(
            model_name='drillcoresample',
            constraint=models.CheckConstraint(check=models.Q(ni__gte=0), name='ni_min_0_drillcore'),
        ),
        migrations.AddConstraint(
            model_name='drillcoresample',
            constraint=models.CheckConstraint(check=models.Q(sc__gte=0), name='sc_min_0_drillcore'),
        ),
        migrations.AddConstraint(
            model_name='drillcoresample',
            constraint=models.CheckConstraint(check=models.Q(si__gte=0), name='si_min_0_drillcore'),
        ),
        migrations.AddConstraint(
            model_name='drillcoresample',
            constraint=models.CheckConstraint(check=models.Q(moisture__gte=0), name='moisture_min_0_drillcore'),
        ),
    ]
