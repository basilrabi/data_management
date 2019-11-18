from datetime import datetime
from django.contrib.gis.db import models as gis_models
from django.core.exceptions import ValidationError
from django.db import models

from fleet.models.equipment import TrackedExcavator
from location.models.source import MineBlock, Stockyard
from personnel.models.person import Person
from custom.fields import NameField, SpaceLess

from .piling import PilingMethod

def this_year():
    return datetime.today().year

class Material(models.Model):
    name = SpaceLess(max_length=10, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class MiningSample(models.Model):
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
        # pylint: disable=E1101
        if self.miningsampleincrement_set.all().count() > 0:
            return True
        return False

    def required_trips(self):
        if self.start_collection:
            # pylint: disable=E1101
            return self.piling_method.trip(self.start_collection)

    def trips_without_increment_id(self, increment_id):
        if self.start_collection:
            # pylint: disable=E1101
            return self.miningsampleincrement_set.exclude(id=increment_id) \
                .aggregate(models.Sum('trips'))['trips__sum'] or 0

    def clean(self):
        if self.ready_for_delivery and not self.has_increment():
            raise ValidationError('Sample cannot be ready for delivery '
                                  'without increments.')

    def save(self, *args, **kwargs):
        # pylint: disable=E1101
        if self.has_increment():
            self.start_collection = self.miningsampleincrement_set.all() \
                .order_by('report__date').first().report.date
            self.year = self.start_collection.year
            self.trips = self.miningsampleincrement_set.all() \
                .aggregate(models.Sum('trips'))['trips__sum']
            if self.trips == self.required_trips():
                self.ready_for_delivery = True
            if self.ready_for_delivery:
                self.end_collection = self.miningsampleincrement_set.all() \
                    .order_by('-report__date').first().report.date
                if not hasattr(self, 'assay'):
                    assay = MiningSampleAssay(mining_sample=self)
                    assay.save()
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
            )
        ]

    def __str__(self):
        # pylint: disable=E1101
        return '{}-{}-{:05d}'.format(self.piling_method.name,
                                     self.ridge,
                                     self.series_number)

class MiningSampleAssay(models.Model):
    mining_sample = models.OneToOneField('MiningSample',
                                         on_delete=models.CASCADE,
                                         related_name='assay')
    date_received_for_preparation = models.DateField(null=True, blank=True)
    date_prepared = models.DateField(null=True, blank=True)
    date_received_for_analysis = models.DateField(null=True, blank=True)
    date_analyzed = models.DateField(null=True, blank=True)
    ni = models.DecimalField(
        '%Ni', max_digits=6, decimal_places=4, null=True, blank=True
    )
    fe = models.DecimalField(
        '%Fe', max_digits=6, decimal_places=4, null=True, blank=True
    )
    co = models.DecimalField(
        '%Co', max_digits=6, decimal_places=4, null=True, blank=True
    )
    moisture = models.DecimalField(
        '%H₂O', max_digits=6, decimal_places=4, null=True, blank=True
    )

    def clean(self):
        if self.ni and not self.date_analyzed:
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
        constraints = [
            models.CheckConstraint(check=models.Q(ni__lte=100),
                                   name='ni_max_100'),
            models.CheckConstraint(check=models.Q(fe__lte=100),
                                   name='fe_max_100'),
            models.CheckConstraint(check=models.Q(co__lte=100),
                                   name='co_max_100'),
            models.CheckConstraint(check=models.Q(moisture__lte=100),
                                   name='moisture_max_100'),
            models.CheckConstraint(check=models.Q(ni__gte=0),
                                   name='ni_min_0'),
            models.CheckConstraint(check=models.Q(fe__gte=0),
                                   name='fe_min_0'),
            models.CheckConstraint(check=models.Q(co__gte=0),
                                   name='co_min_0'),
            models.CheckConstraint(check=models.Q(moisture__gte=0),
                                   name='moisture_min_0')
        ]

    def __str__(self):
        return self.mining_sample.__str__()

class MiningSampleIncrement(models.Model):
    sample = models.ForeignKey('MiningSample', on_delete=models.CASCADE)
    report = models.ForeignKey('MiningSampleReport', on_delete=models.CASCADE)
    trips = models.PositiveSmallIntegerField()

    def clean(self):
        # pylint: disable=E1101
        if self.report.material != self.sample.material:
            raise ValidationError('Material classes do not match.')
        if self.report.piling_method != self.sample.piling_method:
            raise ValidationError('Piling method do not match.')
        if self.report.dumping_area != self.sample.dumping_area:
            raise ValidationError('Dumping area do not match.')
        if self.sample.required_trips():
            if self.trips + self.sample.trips_without_increment_id(self.id) > \
                    self.sample.required_trips():
                raise ValidationError('Trips exceeded the required amount.')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # pylint: disable=E1101
        self.sample.save()

    class Meta:
        ordering = ['sample__series_number']
        constraints = [
            models.UniqueConstraint(
                fields=['sample', 'report'],
                name='sample_increment_report_constraint'
            )
        ]

class MiningSampleReport(gis_models.Model):
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
    source = gis_models.MultiPolygonField(srid=3125, null=True, blank=True)
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
        # pylint: disable=E1101
        if self.id:
            for person in self.sampler.all():
                if 'SAMPLER' not in str(person.designation(self.date)):
                    raise ValidationError(
                        '{} is not a SAMPLER'.format(person.__str__())
                    )
        if self.supervisor:
            if 'SUPERVISOR' not in str(self.supervisor.designation(self.date)):
                raise ValidationError(
                    '{} is not a SUPERVISOR'.format(person.__str__())
                )
        if self.foreman:
            if 'FOREMAN' not in str(self.foreman.designation(self.date)):
                raise ValidationError(
                    '{} is not a FOREMAN'.format(person.__str__())
                )
        if self.piling_method:
            if not self.piling_method.trip(self.date):
                raise ValidationError('No required trips set for piling method '
                                      'selected.')

        # TODO: all polygons of 1 report must come from 1 ridge

    class Meta:
        ordering = ['-date', '-shift_collected']
