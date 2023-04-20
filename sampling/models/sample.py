from decimal import Decimal
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import (
    BooleanField,
    CASCADE,
    CharField,
    DateField,
    DecimalField,
    F,
    FileField,
    ForeignKey,
    ManyToManyField,
    Model,
    OneToOneField,
    PROTECT,
    PositiveSmallIntegerField,
    Q,
    SET_NULL,
    Sum,
    TextField,
    UniqueConstraint
)
from django.utils.html import mark_safe
from os import remove
from os.path import join
from custom.functions import Round, get_assay_constraints
from custom.models import Classification, User
from fleet.models.equipment import TrackedExcavator
from location.models.source import Cluster, DrillHole, Stockpile
from personnel.models.person import Person
from shipment.models.dso import Shipment
from .piling import PilingMethod


class Lithology(Classification):
    """
    Rock-type classification. Usually used in drill core sample.
    """
    class Meta:
        verbose_name_plural = 'lithologies'


class AssaySample(Model):
    """
    A model for all samples prepared and analyzed by Assay.
    """
    date_received_for_preparation = DateField(null=True, blank=True)
    date_prepared = DateField(null=True, blank=True)
    date_received_for_analysis = DateField(null=True, blank=True)
    date_analyzed = DateField(null=True, blank=True)
    al = DecimalField(
        '%Al', max_digits=6, decimal_places=4, null=True, blank=True
    )
    al2o3 = DecimalField(
        '%Al₂O₃', max_digits=6, decimal_places=4, null=True, blank=True
    )
    arsenic = DecimalField(
        '%As', max_digits=6, decimal_places=4, null=True, blank=True
    )
    c = DecimalField(
        '%C', max_digits=6, decimal_places=4, null=True, blank=True
    )
    cao = DecimalField(
        '%CaO', max_digits=6, decimal_places=4, null=True, blank=True
    )
    co = DecimalField(
        '%Co', max_digits=6, decimal_places=4, null=True, blank=True
    )
    cr = DecimalField(
        '%Cr', max_digits=6, decimal_places=4, null=True, blank=True
    )
    cr2o3 = DecimalField(
        '%Cr₂O₃', max_digits=6, decimal_places=4, null=True, blank=True
    )
    cu = DecimalField(
        '%Cu', max_digits=6, decimal_places=4, null=True, blank=True
    )
    fe = DecimalField(
        '%Fe', max_digits=6, decimal_places=4, null=True, blank=True
    )
    k = DecimalField(
        '%K', max_digits=6, decimal_places=4, null=True, blank=True
    )
    mg = DecimalField(
        '%Mg', max_digits=6, decimal_places=4, null=True, blank=True
    )
    mgo = DecimalField(
        '%MgO', max_digits=6, decimal_places=4, null=True, blank=True
    )
    mn = DecimalField(
        '%Mn', max_digits=6, decimal_places=4, null=True, blank=True
    )
    ni = DecimalField(
        '%Ni', max_digits=6, decimal_places=4, null=True, blank=True
    )
    p = DecimalField(
        '%P', max_digits=6, decimal_places=4, null=True, blank=True
    )
    pb = DecimalField(
        '%Pb', max_digits=6, decimal_places=4, null=True, blank=True
    )
    s = DecimalField(
        '%S', max_digits=6, decimal_places=4, null=True, blank=True
    )
    sc = DecimalField(
        '%Sc', max_digits=6, decimal_places=4, null=True, blank=True
    )
    si = DecimalField(
        '%Si', max_digits=6, decimal_places=4, null=True, blank=True
    )
    sio2 = DecimalField(
        '%SiO₂', max_digits=6, decimal_places=4, null=True, blank=True
    )
    zn = DecimalField(
        '%Zn', max_digits=6, decimal_places=4, null=True, blank=True
    )
    ignition_loss = DecimalField(
        max_digits=6, decimal_places=4, null=True, blank=True
    )
    moisture = DecimalField(
        '%H₂O', max_digits=6, decimal_places=4, null=True, blank=True
    )

    def has_analysis(self):
        if (
                self.al is not None or \
                self.al2o3 is not None or \
                self.arsenic is not None or \
                self.c is not None or \
                self.cao is not None or \
                self.co is not None or \
                self.cr is not None or \
                self.cr2o3 is not None or \
                self.cu is not None or \
                self.fe is not None or \
                self.k is not None or \
                self.mg is not None or \
                self.mgo is not None or \
                self.mn is not None or \
                self.ni is not None or \
                self.p is not None or \
                self.pb is not None or \
                self.s is not None or \
                self.sc is not None or \
                self.si is not None or \
                self.sio2 is not None or \
                self.zn is not None or \
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
    drill_hole = ForeignKey(DrillHole, on_delete=CASCADE)
    interval_from = DecimalField(max_digits=5, decimal_places=3)
    interval_to = DecimalField(max_digits=5, decimal_places=3)
    lithology = ForeignKey(
        Lithology, null=True, blank=True, on_delete=SET_NULL
    )
    lithology_modified = ForeignKey(
        Lithology,
        null=True,
        blank=True,
        on_delete=SET_NULL,
        related_name='drillcore'
    )
    description = TextField(null=True, blank=True)
    excavated_date = DateField(null=True, blank=True)

    def clean(self):
        self.clean_base()
        if self.drill_hole.drillcoresample_set.filter(
            Q(interval_from__lt=self.interval_to),
            Q(interval_to__gt=self.interval_from)
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
    series_number = PositiveSmallIntegerField()
    material = CharField(max_length=1, null=True, blank=True)
    ridge = CharField(max_length=2, null=True, blank=True)
    dumping_area = ForeignKey(Stockpile, on_delete=CASCADE)
    piling_method = ForeignKey(PilingMethod, on_delete=CASCADE)
    start_collection = DateField(null=True, blank=True)
    month = PositiveSmallIntegerField(null=True, blank=True)
    end_collection = DateField(null=True, blank=True)
    trips = PositiveSmallIntegerField(default=0)
    ready_for_delivery = BooleanField(default=False)

    def has_increment(self):
        try:
            if self.miningsampleincrement_set.all().count() > 0:
                return True
            return False
        except ValueError:
            return False

    def required_trips(self):
        if self.start_collection:
            return self.piling_method.trip(self.start_collection)

    def trips_without_increment_id(self, increment_id):
        if self.start_collection:
            return self.miningsampleincrement_set.exclude(
                id=increment_id
            ).aggregate(Sum('trips'))['trips__sum'] or 0

    def clean(self):
        self.clean_base()
        if self.ready_for_delivery and not self.has_increment():
            raise ValidationError('Sample cannot be ready for delivery without increments.')

    def save(self, *args, **kwargs):
        if self.has_increment():
            self.start_collection = self.miningsampleincrement_set.all().order_by('report__date').first().report.date
            self.year = self.start_collection.year
            self.trips = self.miningsampleincrement_set.all().aggregate(Sum('trips'))['trips__sum']
            if self.trips == self.required_trips():
                self.ready_for_delivery = True
            if self.ready_for_delivery:
                self.end_collection = self.miningsampleincrement_set.all().order_by('-report__date').first().report.date
        super().save(*args, **kwargs)

    class Meta:
        constraints = get_assay_constraints('miningsample') + [
            UniqueConstraint(
                fields=['ridge', 'material', 'month', 'series_number'],
                name='mining_sample_constraint'
            )
        ]
        ordering = ['-start_collection__year', '-month', '-series_number']

    def __str__(self):
        return f'{self.piling_method.name}-{self.ridge}-{self.series_number:05d}'


class MiningSampleIncrement(Model):
    sample = ForeignKey('MiningSample', on_delete=CASCADE)
    report = ForeignKey('MiningSampleReport', on_delete=CASCADE)
    trips = PositiveSmallIntegerField()

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
            UniqueConstraint(
                fields=['sample', 'report'],
                name='sample_increment_report_constraint'
            )
        ]
        ordering = ['sample__series_number']


class MiningSampleReport(Model):
    date = DateField()
    SHIFT = (
        ('D', 'Day'),
        ('N', 'Night'),
        ('M', 'M'),
    )
    shift_collected = CharField(max_length=1, choices=SHIFT)
    piling_method = ForeignKey(PilingMethod, on_delete=CASCADE)
    tx = ManyToManyField(TrackedExcavator, verbose_name='TX')
    source = ForeignKey(
        Cluster, on_delete=SET_NULL, null=True, blank=True
    )
    dumping_area = ForeignKey(Stockpile, on_delete=CASCADE)
    sampler = ManyToManyField(Person, related_name='samplereport', blank=True)
    supervisor = ForeignKey(
        Person,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name='supervisedminingsamplereport'
    )
    foreman = ForeignKey(
        Person,
        on_delete=SET_NULL,
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


class ApprovedShipmentDischargeAssay(Model):
    assay = OneToOneField('ShipmentDischargeAssay', on_delete=PROTECT)
    approved = BooleanField()
    certificate = FileField(
        upload_to='assay/shipment/discharging/', null=True, blank=True
    )

    def approved_certificate(self):
        if self.certificate:
            return mark_safe(
                '<a class="grp-button" '
                'href="{}" '
                'target="_blank"'
                '>'
                'View Certificate'
                '</a>'.format(self.certificate.url)
            )

    def save(self, *args, **kwargs):
        if ApprovedShipmentDischargeAssay.objects.filter(id=self.id).exists():
            old_file = ApprovedShipmentDischargeAssay.objects.get(id=self.id).certificate
        else:
            old_file = None
        super().save(*args, **kwargs)
        if old_file:
            new_file = ApprovedShipmentDischargeAssay.objects.get(id=self.id).certificate
            if new_file:
                if new_file.name != old_file.name:
                    remove(join(settings.MEDIA_ROOT, old_file.name))
            else:
                remove(join(settings.MEDIA_ROOT, old_file.name))

    class Meta:
        ordering = [
            F('approved').asc(nulls_first=True),
            '-assay__shipment__laydaysstatement__completed_loading'
        ]

    def __str__(self):
        return self.assay.__str__()


class ShipmentDischargeAssay(AssaySample):
    laboratory = ForeignKey(Laboratory, on_delete=PROTECT)
    shipment = OneToOneField(Shipment, on_delete=PROTECT)
    wmt = DecimalField(
        'WMT', null=True, blank=True, max_digits=8, decimal_places=3
    )
    dmt = DecimalField(
        'DMT', null=True, blank=True, max_digits=8, decimal_places=3
    )
    ni_ton = DecimalField(
        'Ni-ton', null=True, blank=True, max_digits=7, decimal_places=3
    )

    def approved_certificate(self):
        if hasattr(self, 'approvedshipmentdischargeassay'):
            if self.approvedshipmentdischargeassay.certificate:
                return self.approvedshipmentdischargeassay.approved_certificate()

    def clean(self):
        if hasattr(self, 'approvedshipmentdischargeassay'):
            if self.approvedshipmentdischargeassay.approved:
                raise ValidationError('Approved assay cannot be changed.')

    def save(self, *args, **kwargs):
        if self.laboratory.name == 'PAMCO':
            try:
                qs = self.shipmentdischargelotassay_set.all()
                if qs.count() > 0:
                    qs = qs \
                        .annotate(dmt=Round(F('wmt') * (100 - F('moisture')) * Decimal(0.01), 3)) \
                        .annotate(ni_ton=Round(F('dmt') * F('ni') * Decimal(0.01), 3)) \
                        .aggregate(Sum('wmt'), Sum('dmt'), Sum('ni_ton'))
                    self.wmt = qs['wmt__sum']
                    self.dmt = qs['dmt__sum']
                    if self.wmt and self.dmt:
                        self.moisture = round((1 - (self.dmt / self.wmt)) * 100, 2)
                        self.ni_ton = qs['ni_ton__sum']
                        if self.ni_ton:
                            self.ni = round(self.ni_ton * 100 / self.dmt, 2)
            except ValueError:
                pass
        else:
            if (self.dmt and self.wmt) and not self.moisture:
                self.moisture = round((1 - (self.dmt / self.wmt)) * 100, 2)
            if (self.wmt and self.moisture) and not self.dmt:
                  self.dmt = round(float(self.wmt * (100 - self.moisture)) * 0.01, 3)
            if self.dmt and self.ni:
                self.ni_ton = round(float(self.ni) * float(self.dmt) * 0.01, 3)
        super().save(*args, **kwargs)
        if not hasattr(self, 'approvedshipmentdischargeassay'):
            approval = ApprovedShipmentDischargeAssay(assay=self, approved=False)
            approval.save()

    class Meta:
        constraints = get_assay_constraints('dischargeassay')
        ordering = ['-shipment__laydaysstatement__completed_loading']

    def __str__(self):
        return self.shipment.__str__()


class ShipmentDischargeLotAssay(AssaySample):
    """
    Only used by PAMCO laboratory. No lot assays are seen in China discharge port asssays.
    """
    shipment_assay = ForeignKey(ShipmentDischargeAssay, on_delete=CASCADE)
    lot = PositiveSmallIntegerField()
    wmt = DecimalField('WMT', max_digits=8, decimal_places=3)

    def dmt(self):
        if self.wmt and self.moisture:
            return round(self.wmt * (100 - self.moisture) / 100, 3)

    def ni_ton(self):
        if self.dmt() and self.ni:
            return round(self.dmt() * self.ni / 100, 3)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.shipment_assay.save()

    class Meta:
        constraints = get_assay_constraints('dischargelotassay') + [
            UniqueConstraint(
                fields=['shipment_assay', 'lot'],
                name='unique_pamco_assay_lot'
            )
        ]
        ordering = ['lot']


class ApprovedShipmentLoadingAssay(Model):
    assay = OneToOneField('ShipmentLoadingAssay', on_delete=PROTECT)
    approved = BooleanField()
    certificate = FileField(
        upload_to='assay/shipment/loading/', null=True, blank=True
    )
    mgb_receipt = FileField(
        upload_to='assay/shipment/loading_receipt', null=True, blank=True
    )

    def PDF(self):
        return self.assay.PDF()

    def approved_certificate(self):
        if self.certificate:
            return mark_safe(
                '<a class="grp-button" '
                'href="{}" '
                'target="_blank"'
                '>'
                'View Certificate'
                '</a>'.format(self.certificate.url)
            )

    def mgb_receiving(self):
        if self.mgb_receipt:
            return mark_safe(
                '<a class="grp-button" '
                'href="{}" '
                'target="_blank"'
                '>'
                'View Acknowledgement'
                '</a>'.format(self.mgb_receipt.url)
            )

    def save(self, *args, **kwargs):
        if ApprovedShipmentLoadingAssay.objects.filter(id=self.id).exists():
            old_file = ApprovedShipmentLoadingAssay.objects.get(id=self.id).certificate
        else:
            old_file = None
        super().save(*args, **kwargs)
        if old_file:
            new_file = ApprovedShipmentLoadingAssay.objects.get(id=self.id).certificate
            if new_file:
                if new_file.name != old_file.name:
                    remove(join(settings.MEDIA_ROOT, old_file.name))
            else:
                remove(join(settings.MEDIA_ROOT, old_file.name))

    class Meta:
        ordering = [
            F('approved').asc(nulls_first=True),
            '-assay__shipment__laydaysstatement__completed_loading'
        ]

    def __str__(self):
        return self.assay.__str__()


class ShipmentLoadingAssay(AssaySample):
    date = DateField()
    shipment = OneToOneField(Shipment, on_delete=CASCADE)
    wmt = DecimalField(
        'WMT', null=True, blank=True, max_digits=8, decimal_places=3
    )
    dmt = DecimalField(
        'DMT', null=True, blank=True, max_digits=8, decimal_places=3
    )
    ni_ton = DecimalField(
        'Ni-ton', null=True, blank=True, max_digits=7, decimal_places=3
    )
    chemist = ForeignKey(User, null=True, blank=True, on_delete=SET_NULL)

    def approved_certificate(self):
        if hasattr(self, 'approvedshipmentloadingassay'):
            if self.approvedshipmentloadingassay.certificate:
                return self.approvedshipmentloadingassay.approved_certificate()

    def clean(self):
        if hasattr(self, 'approvedshipmentloadingassay'):
            if self.approvedshipmentloadingassay.approved:
                raise ValidationError('Approved assay cannot be changed.')

    def PDF(self):
        return mark_safe(
            '<a class="grp-button" '
            'href="/sampling/assay/{}" '
            'target="_blank"'
            '>'
            'View Certificate'
            '</a>'.format(self.shipment.name)
        )

    def bc(self):
        if self.mgo and self.sio2:
            return self.mgo / self.sio2

    def save(self, *args, **kwargs):
        try:
            qs = self.shipmentloadinglotassay_set.all() \
                .annotate(dmt=Round(F('wmt') * (100 - F('moisture')) * Decimal(0.01), 3)) \
                .annotate(ni_ton=Round(F('dmt') * F('ni') * Decimal(0.01), 3)) \
                .aggregate(Sum('wmt'), Sum('dmt'), Sum('ni_ton'))
            self.wmt = qs['wmt__sum']
            self.dmt = qs['dmt__sum']
            if self.wmt and self.dmt:
                self.moisture = round((1 - (self.dmt / self.wmt)) * 100, 2)
                self.ni_ton = qs['ni_ton__sum']
                if self.ni_ton:
                    self.ni = round(self.ni_ton * 100 / self.dmt, 2)
        except ValueError:
            pass
        super().save(*args, **kwargs)
        if not hasattr(self, 'approvedshipmentloadingassay'):
            approval = ApprovedShipmentLoadingAssay(assay=self, approved=False)
            approval.save()

    class Meta:
        constraints = get_assay_constraints('loadingassay')
        ordering = ['-shipment__laydaysstatement__completed_loading']

    def __str__(self):
        return self.shipment.__str__()


class ShipmentLoadingLotAssay(AssaySample):
    shipment_assay = ForeignKey(ShipmentLoadingAssay, on_delete=CASCADE)
    lot = PositiveSmallIntegerField()
    wmt = DecimalField('WMT', max_digits=8, decimal_places=3)

    def dmt(self):
        if self.wmt and self.moisture:
            return round(float(self.wmt) * float(100 - self.moisture) * 0.01, 3)

    def ni_ton(self):
        if self.dmt() and self.ni:
            return round(float(self.dmt()) * float(self.ni) * 0.01, 3)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.shipment_assay.save()

    class Meta:
        constraints = get_assay_constraints('loadinglotassay') + [
            UniqueConstraint(
                fields=['shipment_assay', 'lot'],
                name='unique_loading_assay_lot'
            )
        ]
        ordering = ['lot']
