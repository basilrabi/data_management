from django.core.exceptions import ValidationError
from django.db import models

from custom.fields import NameField, SpaceLess
from custom.functions import this_year
from fleet.models.equipment import TrackedExcavator
from location.models.source import Cluster, DrillHole, MineBlock, Stockyard
from personnel.models.person import Person

from .piling import PilingMethod

# pylint: disable=no-member

class Classification(models.Model):
    """
    Template for any classification.
    """
    name = SpaceLess(max_length=10, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name

class Lithology(Classification):
    """
    Rock-type classification. Usually used in drill core sample.
    """
    pass

class Material(Classification):
    """
    Ore classification
    """
    pass

class AssaySample(models.Model):
    """
    A model for all samples prepared and analyzed by Assay.
    """

    date_received_for_preparation = models.DateField(null=True, blank=True)
    date_prepared = models.DateField(null=True, blank=True)
    date_received_for_analysis = models.DateField(null=True, blank=True)
    date_analyzed = models.DateField(null=True, blank=True)
    al = models.DecimalField('%Al', max_digits=6, decimal_places=4, null=True, blank=True)
    c = models.DecimalField('%C', max_digits=6, decimal_places=4, null=True, blank=True)
    co = models.DecimalField('%Co', max_digits=6, decimal_places=4, null=True, blank=True)
    cr = models.DecimalField('%Cr', max_digits=6, decimal_places=4, null=True, blank=True)
    fe = models.DecimalField('%Fe', max_digits=6, decimal_places=4, null=True, blank=True)
    mg = models.DecimalField('%Mg', max_digits=6, decimal_places=4, null=True, blank=True)
    ni = models.DecimalField('%Ni', max_digits=6, decimal_places=4, null=True, blank=True)
    sc = models.DecimalField('%Sc', max_digits=6, decimal_places=4, null=True, blank=True)
    si = models.DecimalField('%Si', max_digits=6, decimal_places=4, null=True, blank=True)
    moisture = models.DecimalField('%H₂O', max_digits=6, decimal_places=4, null=True, blank=True)

    def has_analysis(self):
        if (
                self.al is not None or \
                self.c is not None or \
                self.co is not None or \
                self.cr is not None or \
                self.fe is not None or \
                self.mg is not None or \
                self.ni is not None or \
                self.sc is not None or \
                self.si is not None or \
                self.moisture is not None
        ):
            return True
        return False

    def clean_base(self):
        if self.has_analysis() and not self.date_analyzed:
            raise ValidationError('Date of analysis required.')
        if self.date_analyzed and not self.date_received_for_analysis:
            raise ValidationError('Date of receiving for analysis required.')
        if self.date_received_for_analysis and not self.date_prepared:
            raise ValidationError('Date of preparation required.')
        if self.date_prepared and not self.date_received_for_preparation:
            raise ValidationError('Date of receiving for preparation required.')
        if self.date_analyzed:
            if self.date_analyzed < self.date_received_for_analysis:
                raise ValidationError('Date of receiving for analysis must be '
                                      'earlier than analyzed date.')
            if self.date_received_for_analysis < self.date_prepared:
                raise ValidationError('Date of preparation must be earlier '
                                      'than date of receiving for analysis.')
            if self.date_prepared < self.date_received_for_preparation:
                raise ValidationError('Date of receiving for preparation must '
                                      'be earlier than date of preparation.')

    class Meta:
        abstract = True

class DrillCoreSample(AssaySample):
    drill_hole = models.ForeignKey(DrillHole, on_delete=models.CASCADE)
    interval_from = models.DecimalField(max_digits=5, decimal_places=3)
    interval_to = models.DecimalField(max_digits=5, decimal_places=3)
    lithology = models.ForeignKey(
        Lithology, null=True, blank=True, on_delete=models.SET_NULL
    )
    description = models.TextField()

    def clean(self):
        self.clean_base()

    class Meta:
        ordering = ['interval_from']
        constraints = [
            models.CheckConstraint(check=models.Q(al__lte=100), name='al_max_100_drillcore'),
            models.CheckConstraint(check=models.Q(c__lte=100), name='c_max_100_drillcore'),
            models.CheckConstraint(check=models.Q(co__lte=100), name='co_max_100_drillcore'),
            models.CheckConstraint(check=models.Q(cr__lte=100), name='cr_max_100_drillcore'),
            models.CheckConstraint(check=models.Q(fe__lte=100), name='fe_max_100_drillcore'),
            models.CheckConstraint(check=models.Q(mg__lte=100), name='mg_max_100_drillcore'),
            models.CheckConstraint(check=models.Q(ni__lte=100), name='ni_max_100_drillcore'),
            models.CheckConstraint(check=models.Q(sc__lte=100), name='sc_max_100_drillcore'),
            models.CheckConstraint(check=models.Q(si__lte=100), name='si_max_100_drillcore'),
            models.CheckConstraint(check=models.Q(moisture__lte=100), name='moisture_max_100_drillcore'),
            models.CheckConstraint(check=models.Q(al__gte=0), name='al_min_0_drillcore'),
            models.CheckConstraint(check=models.Q(c__gte=0), name='c_min_0_drillcore'),
            models.CheckConstraint(check=models.Q(co__gte=0), name='co_min_0_drillcore'),
            models.CheckConstraint(check=models.Q(cr__gte=0), name='cr_min_0_drillcore'),
            models.CheckConstraint(check=models.Q(fe__gte=0), name='fe_min_0_drillcore'),
            models.CheckConstraint(check=models.Q(mg__gte=0), name='mg_min_0_drillcore'),
            models.CheckConstraint(check=models.Q(ni__gte=0), name='ni_min_0_drillcore'),
            models.CheckConstraint(check=models.Q(sc__gte=0), name='sc_min_0_drillcore'),
            models.CheckConstraint(check=models.Q(si__gte=0), name='si_min_0_drillcore'),
            models.CheckConstraint(check=models.Q(moisture__gte=0), name='moisture_min_0_drillcore')
        ]

class MiningSample(AssaySample):
    series_number = models.PositiveSmallIntegerField()
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    ridge = models.CharField(max_length=2, null=True, blank=True)
    dumping_area = models.ForeignKey(Stockyard, on_delete=models.CASCADE)
    piling_method = models.ForeignKey(PilingMethod, on_delete=models.CASCADE)
    start_collection = models.DateField(null=True, blank=True)
    year = models.PositiveSmallIntegerField(default=this_year)
    end_collection = models.DateField(null=True, blank=True)
    trips = models.PositiveSmallIntegerField(default=0)
    ready_for_delivery = models.BooleanField(default=False)
    harvested = models.BooleanField(default=False)

    def has_increment(self):
        if self.miningsampleincrement_set.all().count() > 0:
            return True
        return False

    def required_trips(self):
        if self.start_collection:
            return self.piling_method.trip(self.start_collection)

    def trips_without_increment_id(self, increment_id):
        if self.start_collection:
            return self.miningsampleincrement_set.exclude(id=increment_id).aggregate(models.Sum('trips'))['trips__sum'] or 0

    def clean(self):
        self.clean_base()
        if self.ready_for_delivery and not self.has_increment():
            raise ValidationError('Sample cannot be ready for delivery without increments.')

    def save(self, *args, **kwargs):
        if self.has_increment():
            self.start_collection = self.miningsampleincrement_set.all().order_by('report__date').first().report.date
            self.year = self.start_collection.year
            self.trips = self.miningsampleincrement_set.all().aggregate(models.Sum('trips'))['trips__sum']
            if self.trips == self.required_trips():
                self.ready_for_delivery = True
            if self.ready_for_delivery:
                self.end_collection = self.miningsampleincrement_set.all().order_by('-report__date').first().report.date
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-start_collection__year', '-series_number']
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'ridge',
                    'year',
                    'piling_method',
                    'series_number'
                ],
                name='mining_sample_series_constraint'
            ),
            models.CheckConstraint(check=models.Q(al__lte=100), name='al_max_100_miningsample'),
            models.CheckConstraint(check=models.Q(c__lte=100), name='c_max_100_miningsample'),
            models.CheckConstraint(check=models.Q(co__lte=100), name='co_max_100_miningsample'),
            models.CheckConstraint(check=models.Q(cr__lte=100), name='cr_max_100_miningsample'),
            models.CheckConstraint(check=models.Q(fe__lte=100), name='fe_max_100_miningsample'),
            models.CheckConstraint(check=models.Q(mg__lte=100), name='mg_max_100_miningsample'),
            models.CheckConstraint(check=models.Q(ni__lte=100), name='ni_max_100_miningsample'),
            models.CheckConstraint(check=models.Q(sc__lte=100), name='sc_max_100_miningsample'),
            models.CheckConstraint(check=models.Q(si__lte=100), name='si_max_100_miningsample'),
            models.CheckConstraint(check=models.Q(moisture__lte=100), name='moisture_max_100_miningsample'),
            models.CheckConstraint(check=models.Q(al__gte=0), name='al_min_0_miningsample'),
            models.CheckConstraint(check=models.Q(c__gte=0), name='c_min_0_miningsample'),
            models.CheckConstraint(check=models.Q(co__gte=0), name='co_min_0_miningsample'),
            models.CheckConstraint(check=models.Q(cr__gte=0), name='cr_min_0_miningsample'),
            models.CheckConstraint(check=models.Q(fe__gte=0), name='fe_min_0_miningsample'),
            models.CheckConstraint(check=models.Q(mg__gte=0), name='mg_min_0_miningsample'),
            models.CheckConstraint(check=models.Q(ni__gte=0), name='ni_min_0_miningsample'),
            models.CheckConstraint(check=models.Q(sc__gte=0), name='sc_min_0_miningsample'),
            models.CheckConstraint(check=models.Q(si__gte=0), name='si_min_0_miningsample'),
            models.CheckConstraint(check=models.Q(moisture__gte=0), name='moisture_min_0_miningsample')
        ]

    def __str__(self):
        return f'{self.piling_method.name}-{self.ridge}-{self.series_number:05d}'

class MiningSampleIncrement(models.Model):
    sample = models.ForeignKey('MiningSample', on_delete=models.CASCADE)
    report = models.ForeignKey('MiningSampleReport', on_delete=models.CASCADE)
    trips = models.PositiveSmallIntegerField()

    def clean(self):
        if self.report.material != self.sample.material:
            raise ValidationError('Material classes do not match.')
        if self.report.piling_method != self.sample.piling_method:
            raise ValidationError('Piling method do not match.')
        if self.report.dumping_area != self.sample.dumping_area:
            raise ValidationError('Dumping area do not match.')
        if self.sample.required_trips():
            if self.trips + self.sample.trips_without_increment_id(self.id) > self.sample.required_trips():
                raise ValidationError('Trips exceeded the required amount.')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.sample.save()

    class Meta:
        ordering = ['sample__series_number']
        constraints = [
            models.UniqueConstraint(
                fields=['sample', 'report'],
                name='sample_increment_report_constraint'
            )
        ]

class MiningSampleReport(models.Model):
    date = models.DateField()
    SHIFT = (
        ('D', 'Day'),
        ('N', 'Night'),
        ('M', 'M'),
    )
    shift_collected = models.CharField(max_length=1, choices=SHIFT)
    piling_method = models.ForeignKey(PilingMethod, on_delete=models.CASCADE)
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    tx = models.ForeignKey(TrackedExcavator,
                           on_delete=models.CASCADE,
                           verbose_name='TX')
    source = models.ForeignKey(
        Cluster, on_delete=models.SET_NULL, null=True, blank=True
    )
    dumping_area = models.ForeignKey(Stockyard, on_delete=models.CASCADE)
    sampler = models.ManyToManyField(Person,
                                     related_name='samplereport',
                                     blank=True)
    supervisor = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='supervisedminingsamplereport'
    )
    foreman = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managedminingsamplereport'
    )

    def clean(self):
        if self.id:
            for person in self.sampler.all():
                if 'SAMPLER' not in str(person.designation(self.date)):
                    raise ValidationError(
                        f'{person.__str__()} is not a SAMPLER'
                    )
        if self.supervisor:
            if 'SUPERVISOR' not in str(self.supervisor.designation(self.date)):
                raise ValidationError(
                    f'{person.__str__()} is not a SUPERVISOR'
                )
        if self.foreman:
            if 'FOREMAN' not in str(self.foreman.designation(self.date)):
                raise ValidationError(
                    f'{person.__str__()} is not a FOREMAN'
                )
        if self.piling_method:
            if not self.piling_method.trip(self.date):
                raise ValidationError('No required trips set for piling method selected.')

    class Meta:
        ordering = ['-date', '-shift_collected']
