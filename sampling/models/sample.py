from django.core.exceptions import ValidationError
from django.db import models

from custom.fields import NameField
from custom.functions import Round, get_assay_constraints, this_year
from custom.models import Classification
from fleet.models.equipment import TrackedExcavator
from location.models.source import Cluster, DrillHole, MineBlock, Stockpile
from personnel.models.person import Person
from shipment.models.dso import Shipment

from .piling import PilingMethod

# pylint: disable=no-member


class Lithology(Classification):
    """
    Rock-type classification. Usually used in drill core sample.
    """
    class Meta:
        verbose_name_plural = 'lithologies'


class AssaySample(models.Model):
    """
    A model for all samples prepared and analyzed by Assay.
    """
    date_received_for_preparation = models.DateField(null=True, blank=True)
    date_prepared = models.DateField(null=True, blank=True)
    date_received_for_analysis = models.DateField(null=True, blank=True)
    date_analyzed = models.DateField(null=True, blank=True)
    al = models.DecimalField('%Al', max_digits=6, decimal_places=4, null=True, blank=True)
    al2o3 = models.DecimalField('%Al₂O₃', max_digits=6, decimal_places=4, null=True, blank=True)
    c = models.DecimalField('%C', max_digits=6, decimal_places=4, null=True, blank=True)
    cao = models.DecimalField('%CaO', max_digits=6, decimal_places=4, null=True, blank=True)
    co = models.DecimalField('%Co', max_digits=6, decimal_places=4, null=True, blank=True)
    cr = models.DecimalField('%Cr', max_digits=6, decimal_places=4, null=True, blank=True)
    fe = models.DecimalField('%Fe', max_digits=6, decimal_places=4, null=True, blank=True)
    mg = models.DecimalField('%Mg', max_digits=6, decimal_places=4, null=True, blank=True)
    mgo = models.DecimalField('%MgO', max_digits=6, decimal_places=4, null=True, blank=True)
    mn = models.DecimalField('%Mn', max_digits=6, decimal_places=4, null=True, blank=True)
    ni = models.DecimalField('%Ni', max_digits=6, decimal_places=4, null=True, blank=True)
    p = models.DecimalField('%P', max_digits=6, decimal_places=4, null=True, blank=True)
    s = models.DecimalField('%S', max_digits=6, decimal_places=4, null=True, blank=True)
    sc = models.DecimalField('%Sc', max_digits=6, decimal_places=4, null=True, blank=True)
    si = models.DecimalField('%Si', max_digits=6, decimal_places=4, null=True, blank=True)
    sio2 = models.DecimalField('%SiO₂', max_digits=6, decimal_places=4, null=True, blank=True)
    ignition_loss = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    moisture = models.DecimalField('%H₂O', max_digits=6, decimal_places=4, null=True, blank=True)

    def has_analysis(self):
        if (
                self.al is not None or \
                self.al2o3 is not None or \
                self.c is not None or \
                self.cao is not None or \
                self.co is not None or \
                self.cr is not None or \
                self.fe is not None or \
                self.mg is not None or \
                self.mgo is not None or \
                self.mn is not None or \
                self.ni is not None or \
                self.p is not None or \
                self.s is not None or \
                self.sc is not None or \
                self.si is not None or \
                self.sio2 is not None or \
                self.ignition_loss is not None or \
                self.moisture is not None
        ):
            return True
        return False

    def bc(self):
        if self.mgo and self.sio2:
            return round(self.mgo / self.sio2, 2)

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
    description = models.TextField(null=True, blank=True)
    excavated_date = models.DateField(null=True, blank=True)

    def clean(self):
        self.clean_base()
        if self.drill_hole.drillcoresample_set.filter(
            models.Q(interval_from__lt=self.interval_to),
            models.Q(interval_to__gt=self.interval_from)
        ).exclude(id=self.id).count() > 0:
            raise ValidationError('Core interval should not overlap')
        if float(self.interval_from) >= float(self.interval_to):
            raise ValidationError('interval_to should be greater than interval_from')

    class Meta:
        constraints = get_assay_constraints('drillcore')
        ordering = ['interval_from']


class Laboratory(Classification):
    class Meta:
        verbose_name_plural = 'laboratories'


class MiningSample(AssaySample):
    series_number = models.PositiveSmallIntegerField()
    material = models.CharField(max_length=1, null=True, blank=True)
    ridge = models.CharField(max_length=2, null=True, blank=True)
    dumping_area = models.ForeignKey(Stockpile, on_delete=models.CASCADE)
    piling_method = models.ForeignKey(PilingMethod, on_delete=models.CASCADE)
    start_collection = models.DateField(null=True, blank=True)
    month = models.PositiveSmallIntegerField(null=True, blank=True)
    end_collection = models.DateField(null=True, blank=True)
    trips = models.PositiveSmallIntegerField(default=0)
    ready_for_delivery = models.BooleanField(default=False)

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
        constraints = get_assay_constraints('miningsample') + [
            models.UniqueConstraint(
                fields=['ridge', 'material', 'month', 'series_number'],
                name='mining_sample_constraint'
            )
        ]
        ordering = ['-start_collection__year', '-month', '-series_number']

    def __str__(self):
        return f'{self.piling_method.name}-{self.ridge}-{self.series_number:05d}'


class MiningSampleIncrement(models.Model):
    sample = models.ForeignKey('MiningSample', on_delete=models.CASCADE)
    report = models.ForeignKey('MiningSampleReport', on_delete=models.CASCADE)
    trips = models.PositiveSmallIntegerField()

    def clean(self):
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
        constraints = [
            models.UniqueConstraint(
                fields=['sample', 'report'],
                name='sample_increment_report_constraint'
            )
        ]
        ordering = ['sample__series_number']


class MiningSampleReport(models.Model):
    date = models.DateField()
    SHIFT = (
        ('D', 'Day'),
        ('N', 'Night'),
        ('M', 'M'),
    )
    shift_collected = models.CharField(max_length=1, choices=SHIFT)
    piling_method = models.ForeignKey(PilingMethod, on_delete=models.CASCADE)
    tx = models.ManyToManyField(TrackedExcavator, verbose_name='TX')
    source = models.ForeignKey(
        Cluster, on_delete=models.SET_NULL, null=True, blank=True
    )
    dumping_area = models.ForeignKey(Stockpile, on_delete=models.CASCADE)
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


class ShipmentDischargeAssay(AssaySample):
    laboratory = models.ForeignKey(Laboratory, on_delete=models.PROTECT)
    shipment = models.OneToOneField(Shipment, on_delete=models.PROTECT)
    wmt = models.DecimalField('WMT', null=True, blank=True, max_digits=8, decimal_places=3)
    dmt = models.DecimalField('DMT', null=True, blank=True, max_digits=8, decimal_places=3)

    def save(self, *args, **kwargs):
        if self.laboratory.name == 'PAMCO':
            qs = self.shipmentdischargelotassay_set.all() \
                .annotate(dmt=Round(models.F('wmt') * (100 - models.F('moisture')) * 0.01, 3)) \
                .annotate(ni_ton=Round(models.F('dmt') * models.F('ni') * 0.01, 3)) \
                .aggregate(models.Sum('wmt'), models.Sum('dmt'), models.Sum('ni_ton'))
            self.wmt = qs['wmt__sum']
            self.dmt = qs['dmt__sum']
            if self.wmt and self.dmt:
                self.moisture = round((1 - (self.dmt / self.wmt)) * 100, 2)
                self.ni_ton = qs['ni_ton__sum']
                if self.ni_ton:
                    self.ni = round(self.ni_ton * 100 / self.dmt, 2)
        else:
            if (self.dmt and self.wmt) and not self.moisture:
                self.moisture = round((1 - (self.dmt / self.wmt)) * 100, 2)
            if (self.wmt and self.moisture) and not self.dmt:
                self.dmt = round(float(self.wmt * (100 - self.moisture)) * 0.01, 3)
        super().save(*args, **kwargs)

    class Meta:
        constraints = get_assay_constraints('dischargeassay')
        ordering = ['-shipment__laydaysstatement__completed_loading']

    def __str__(self):
        return self.shipment.name


class ShipmentDischargeLotAssay(AssaySample):
    """
    Only used by PAMCO laboratory. No lot assays are seen in China discharge port asssays.
    """
    shipment_assay = models.ForeignKey(ShipmentDischargeAssay, on_delete=models.CASCADE)
    lot = models.PositiveSmallIntegerField(unique=True)
    wmt = models.DecimalField('WMT', max_digits=8, decimal_places=3)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.shipment_assay.save()

    class Meta:
        constraints = get_assay_constraints('dischargelotassay') + [
            models.UniqueConstraint(
                fields=['shipment_assay', 'lot'],
                name='unique_pamco_assay_lot'
            )
        ]
        ordering = ['lot']


class ShipmentLoadingAssay(AssaySample):
    date = models.DateField()
    shipment = models.OneToOneField(Shipment, on_delete=models.CASCADE)
    wmt = models.DecimalField('WMT', null=True, blank=True, max_digits=8, decimal_places=3)
    dmt = models.DecimalField('DMT', null=True, blank=True, max_digits=8, decimal_places=3)
    ni_ton = models.DecimalField('Ni-ton', null=True, blank=True, max_digits=7, decimal_places=3)

    def save(self, *args, **kwargs):
        qs = self.shipmentloadinglotassay_set.all() \
            .annotate(dmt=Round(models.F('wmt') * (100 - models.F('moisture')) * 0.01, 3)) \
            .annotate(ni_ton=Round(models.F('dmt') * models.F('ni') * 0.01, 3)) \
            .aggregate(models.Sum('wmt'), models.Sum('dmt'), models.Sum('ni_ton'))
        self.wmt = qs['wmt__sum']
        self.dmt = qs['dmt__sum']
        if self.wmt and self.dmt:
            self.moisture = round((1 - (self.dmt / self.wmt)) * 100, 2)
            self.ni_ton = qs['ni_ton__sum']
            if self.ni_ton:
                self.ni = round(self.ni_ton * 100 / self.dmt, 2)
        super().save(*args, **kwargs)

    class Meta:
        constraints = get_assay_constraints('loadingassay')
        ordering = ['-shipment__laydaysstatement__completed_loading']

    def __str__(self):
        return self.shipment.name


class ShipmentLoadingLotAssay(AssaySample):
    shipment_assay = models.ForeignKey(ShipmentLoadingAssay, on_delete=models.CASCADE)
    lot = models.PositiveSmallIntegerField()
    wmt = models.DecimalField('WMT', max_digits=8, decimal_places=3)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.shipment_assay.save()

    class Meta:
        constraints = get_assay_constraints('loadinglotassay') + [
            models.UniqueConstraint(
                fields=['shipment_assay', 'lot'],
                name='unique_loading_assay_lot'
            )
        ]
        ordering = ['lot']
