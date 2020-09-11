import datetime

from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.html import mark_safe
from django.utils.timezone import now
from re import sub

from custom.fields import AlphaNumeric, NameField, MarineVesselName
from custom.functions import (
    ordinal_suffix, print_localzone, refresh_shipment_number, round_second,
    round_up_day, to_dhms, to_hm, to_hms
)
from custom.models import Classification
from custom.variables import one_day, zero_time

# pylint: disable=no-member


class Buyer(Classification):
    pass


class Destination(Classification):
    """
    Discharging port.
    """
    pass


class LayDaysDetail(models.Model):
    """
    An entry in the laydays statement.
    """
    laydays = models.ForeignKey('LayDaysStatement', on_delete=models.CASCADE)
    interval_from = models.DateTimeField()

    RATE_CHOICES = (
        (100, '100'),
        (80, '80'),
        (75, '75'),
        (50, '50'),
        (25, '25'),
        (0, '0')
    )
    laytime_rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES)

    CLASS_CHOICES = (
        ('continuous loading', 'Continuous Loading'),
        ('sun drying', 'Sun Drying'),
        ('heavy swell', 'Heavy Swell'),
        ('rain', 'Rain'),
        ('rain and heavy swell', 'Rain and Heavy Swell'),
        ('waiting for cargo', 'Waiting for Cargo'),
        ('waiting for cargo due to rejection', 'Waiting for Cargo (rejected)'),
        ('waiting for loading commencement', 'Waiting for Loading Commencement'),
        ('end', 'End'),
        ('vessel arrived behind of schedule', 'Vessel Arrived Behind of Schedule'),
        ('others', '-')
    )
    interval_class = models.CharField(max_length=50, choices=CLASS_CHOICES)
    remarks = models.TextField(null=True, blank=True)

    def interval(self):
        if self.next():
            return self.next().interval_from - self.interval_from

    def next(self):
        return self.laydays.laydaysdetail_set.filter(models.Q(
            interval_from__gt=self.interval_from
        )).order_by('interval_from').first()

    class Meta:
        ordering = ['interval_from']
        constraints = [
            models.UniqueConstraint(
                fields=['laydays', 'interval_from'],
                name='unique_vessel_trip_timestamp'
            ),
            models.UniqueConstraint(
                fields=['laydays', 'interval_class'],
                condition=models.Q(interval_class='end'),
                name='unique_end_laydaysdetail'
            )
        ]


class LayDaysDetailComputed(models.Model):

    laydays = models.ForeignKey('LayDaysStatement', on_delete=models.CASCADE)
    interval_from = models.DateTimeField()
    laytime_rate = models.PositiveSmallIntegerField(
        help_text='Percent available vessel grabs.'
    )
    time_remaining = models.DurationField()
    interval_class = models.CharField(max_length=50)
    remarks = models.TextField(null=True, blank=True)

    def consumed(self):
        """
        Laytime consumption.
        """
        if self.previous():
            return round_second(
                self.interval() * (self.previous().laytime_rate / 100)
            )
        return zero_time

    def consumed_formated(self):
        """
        Laytime consumption formatted in hours:minutes:seconds
        """
        return to_hms(self.consumed())

    def days_consumed(self):
        if self.previous():
            return (self.interval() * (self.previous().laytime_rate / 100)) / one_day
        return 0

    def days_remaining(self):
        return self.time_remaining / one_day

    def interval(self):
        if self.previous():
            return self.interval_from - self.previous().interval_from
        return zero_time

    def interval_formated(self):
        """
        Time interval formatted in hours:minutes
        """
        return to_hm(self.interval())

    def is_new_day(self):
        previous_detail = self.previous()
        if previous_detail:
            if round_up_day(previous_detail.interval_from) > self.interval_from:
                return False
        return True

    def next(self):
        return self.laydays.laydaysdetailcomputed_set.filter(models.Q(
            interval_from__gt=self.interval_from
        )).order_by('interval_from').first()

    def previous(self):
        return self.laydays.laydaysdetailcomputed_set.filter(models.Q(
            interval_from__lt=self.interval_from
        )).order_by('-interval_from').first()

    def remaining(self):
        """
        Time remaining in hms.
        """
        return to_dhms(self.time_remaining)

    class Meta:
        ordering = ['interval_from']


class ApprovedLayDaysStatement(models.Model):
    statement = models.OneToOneField('LayDaysStatement', on_delete=models.PROTECT)
    approved = models.BooleanField()

    def csv(self):
        return self.statement.csv()

    def PDF(self):
        return self.statement.PDF()

    def save(self, *args, **kwargs):
        original_obj = ApprovedLayDaysStatement.objects.filter(id=self.id)
        if original_obj.exists():
            original_obj = original_obj[0]
            if self.approved and not original_obj.approved:
                shipment = self.statement.shipment
                if shipment.demurrage is None and shipment.despatch is None:
                    shipment.demurrage = self.statement.demurrage
                    shipment.despatch = self.statement.despatch
                    shipment.save(refresh=False)
        super().save(*args, **kwargs)


    class Meta:
        ordering = [
            'approved',
            models.F('statement__completed_loading').desc(nulls_last=False),
            models.F('statement__arrival_tmc').desc(nulls_last=False)
        ]

    def __str__(self):
        return self.statement.__str__()


class LayDaysStatement(models.Model):
    """
    A vessel's laydays statement for a shipment loading.
    """
    shipment = models.OneToOneField('Shipment', on_delete=models.CASCADE)
    vessel_voyage = models.PositiveSmallIntegerField(default=0)
    arrival_pilot = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Arrival at Surigao Pilot Station'
    )
    arrival_tmc = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Arrival at TMC Port'
    )
    nor_tender = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Notice of Readiness Tendered'
    )
    nor_accepted = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Notice of Readiness Accepted'
    )
    commenced_laytime = models.DateTimeField(null=True, blank=True)
    commenced_loading = models.DateTimeField(null=True, blank=True)
    completed_loading = models.DateTimeField(null=True, blank=True)
    cargo_description = NameField(max_length=20, default='NICKEL ORE')
    tonnage = models.PositiveIntegerField(null=True, blank=True)
    loading_terms = models.PositiveSmallIntegerField(
        default=6000,
        help_text='Agreed loading rate (tons per day).'
    )
    demurrage_rate = models.PositiveSmallIntegerField(
        default=11000,
        help_text='US Dollar per day'
    )
    despatch_rate = models.PositiveSmallIntegerField(
        default=5500,
        help_text='US Dollar per day'
    )
    can_test = models.PositiveSmallIntegerField(
        default=0,
        help_text='Number of can tests performed.'
    )
    pre_loading_can_test = models.BooleanField(
        default=False,
        help_text='Is can test conducted before commencement of loading?',
        verbose_name='Pre-loading Can Test'
    )
    CAN_TEST_FACTOR_CHOICES = (
        (0.0, '0.0'),
        (0.5, '0.5'),
        (1.0, '1.0')
    )
    can_test_factor = models.DecimalField(
        default=0.5,
        max_digits=2,
        decimal_places=1,
        choices=CAN_TEST_FACTOR_CHOICES,
        help_text="""The number of can tests times this factor times 5 minutes
            will be deducted to laytime consumed."""
    )
    time_allowed = models.DurationField(default=zero_time)
    additional_laytime = models.DurationField(default=zero_time)
    demurrage = models.DecimalField(
        default=0, max_digits=8, decimal_places=2
    )
    despatch = models.DecimalField(
        default=0, max_digits=8, decimal_places=2
    )
    date_saved = models.DateTimeField(null=True, blank=True)
    report_date = models.DateField(
        null=True,
        blank=True,
        help_text='Date of statement. Defaults to date_saved.'
    )
    revised = models.BooleanField(
        default=False,
        help_text='This lay days statement is revised from a previous version.'
    )
    date_computed = models.DateTimeField(null=True, blank=True)
    negotiated = models.BooleanField(
        default=False,
        help_text='Demurrage/Despatch is negotiated.'
    )
    remarks = models.TextField(null=True, blank=True)

    def _clean(self):
        """
        Removes redundant details.
        """
        final = False
        while not final and self.laydaysdetail_set.count() > 1:
            for detail in self.laydaysdetail_set.all():
                if not detail.next():
                    final = True
                    break

                if detail.laytime_rate == detail.next().laytime_rate and \
                        detail.interval_class == detail.next().interval_class and \
                        detail.remarks == detail.next().remarks:
                    detail.next().delete()
                    break

    def _compute(self):
        if not self.date_computed or self.date_saved > self.date_computed:
            self._clean()
            details = self.laydaysdetailcomputed_set.all()
            if details.exists():
                details.delete()
            if self.laydaysdetail_set.all().count() >= 1:
                # Compute additional laytime
                bonus_time = zero_time
                for detail in self.laydaysdetail_set.filter(
                    models.Q(interval_class='vessel arrived behind of schedule')
                ):
                    bonus_time += detail.interval()
                if bonus_time > zero_time:
                    self.additional_laytime = round_second(bonus_time)

                # Record commencement of laytime
                details = self.laydaysdetail_set.exclude(interval_class='vessel arrived behind of schedule')
                if details.exists():
                    self.commenced_laytime = details.first().interval_from

                loading_details = self.laydaysdetail_set.filter(interval_class='continuous loading')
                # Proceed computation if loading details exist
                if loading_details.exists():

                    # Record start of loading operation
                    self.commenced_loading = loading_details.first().interval_from
                    if self.pre_loading_can_test:
                        self.commenced_loading += datetime.timedelta(minutes=5)

                    end_details = self.laydaysdetail_set.filter(interval_class='end')
                    #  Proceed computation if end of statement exists.
                    if end_details.exists():

                        # Record end of loading operation.
                        self.completed_loading = loading_details.last().next().interval_from

                        _time_remaining = self.time_limit() + self.additional_laytime
                        self.time_allowed = _time_remaining
                        NATURAL_DELAYS = [
                            'heavy swell',
                            'rain',
                            'rain and heavy swell',
                            'vessel arrived behind of schedule'
                        ]
                        for detail in self.laydaysdetail_set.all():

                            # Create initial computed detail object copied from the orignal detail.
                            computed_detail = LayDaysDetailComputed(
                                laydays=detail.laydays,
                                interval_from=detail.interval_from,
                                laytime_rate=detail.laytime_rate,
                                interval_class=detail.interval_class,
                                remarks=detail.remarks
                            )

                            # If laytime rates are mistakenly set, adjust.
                            if (_time_remaining - computed_detail.consumed()) > zero_time and \
                                    detail.interval_class in NATURAL_DELAYS and \
                                    detail.laytime_rate > 0:
                                detail.laytime_rate = 0
                                detail.save()
                                computed_detail.laytime_rate = 0
                            if (_time_remaining - computed_detail.consumed()) <= zero_time and \
                                    detail.interval_class in NATURAL_DELAYS and \
                                    detail.laytime_rate < 100:
                                detail.laytime_rate = 100
                                detail.save()
                                computed_detail.laytime_rate = 100

                            previous_detail = computed_detail.previous()
                            if previous_detail:

                                # Check whether the time interval between the previous saved detail and the present detail crosses midnight.
                                # If the interval crosses midnight, create a new time stamp at midnight after the previous detail.
                                if round_up_day(previous_detail.interval_from) < detail.interval_from:
                                    while round_up_day(previous_detail.interval_from) < detail.interval_from:

                                        # Create a new time stamp by incrementing the previous time stamp
                                        computed_detail_virtual = LayDaysDetailComputed(
                                            laydays=detail.laydays,
                                            interval_from=round_up_day(previous_detail.interval_from),
                                            laytime_rate=previous_detail.laytime_rate,
                                            interval_class=previous_detail.interval_class
                                        )
                                        time_remaining = _time_remaining - computed_detail_virtual.consumed()

                                        # During lay time expiry while using virtual time stamp, save a time stamp at the end of allowed laytime.
                                        if _time_remaining > zero_time and time_remaining < zero_time:
                                            computed_detail_virtual.interval_from = previous_detail.interval_from + (
                                                round_second(
                                                    _time_remaining / (computed_detail_virtual.previous().laytime_rate / 100)
                                                )
                                            )
                                            computed_detail_virtual.remarks = 'laytime expires'
                                            computed_detail_virtual.time_remaining = zero_time
                                            _time_remaining = zero_time

                                        # Save time stamp at midnight
                                        else:
                                            computed_detail_virtual.interval_from = round_up_day(previous_detail.interval_from)
                                            computed_detail_virtual.time_remaining = time_remaining
                                            _time_remaining = time_remaining

                                        computed_detail_virtual.save()
                                        previous_detail = self.laydaysdetailcomputed_set.last()

                                    # If while approaching the actual time stamp, the lay time expires, save a time stamp at the end of allowed laytime.
                                    if _time_remaining > zero_time and computed_detail.consumed() > _time_remaining:
                                        computed_detail_virtual = LayDaysDetailComputed(
                                            laydays=detail.laydays,
                                            interval_from=previous_detail.interval_from + (
                                                round_second(
                                                    _time_remaining / (previous_detail.laytime_rate / 100)
                                                )
                                            ),
                                            laytime_rate=previous_detail.laytime_rate,
                                            interval_class=previous_detail.interval_class,
                                            remarks='laytime expires',
                                            time_remaining=zero_time
                                        )
                                        computed_detail_virtual.save()
                                        _time_remaining = zero_time

                                # If the previous time interval does not cross midnight, save the present detail as new computed detail.
                                time_remaining = _time_remaining - computed_detail.consumed()

                                if _time_remaining > zero_time and time_remaining == zero_time:
                                    computed_detail.time_remaining = time_remaining
                                    computed_detail.remarks='laytime expires'
                                    computed_detail.save()
                                    _time_remaining = time_remaining
                                    continue

                                # During lay time expiry, save a time stamp at the end of allowed laytime.
                                if _time_remaining > zero_time and time_remaining < zero_time:
                                    computed_detail_virtual = LayDaysDetailComputed(
                                        laydays=detail.laydays,
                                        interval_from=previous_detail.interval_from + round_second(_time_remaining / (previous_detail.laytime_rate / 100)),
                                        laytime_rate=previous_detail.laytime_rate,
                                        interval_class=previous_detail.interval_class,
                                        remarks='laytime expires',
                                        time_remaining=zero_time
                                    )
                                    computed_detail_virtual.save()

                                computed_detail.time_remaining = time_remaining
                                computed_detail.save()
                                _time_remaining = time_remaining

                            # If start of statement, save time stamp right away
                            else:
                                computed_detail.time_remaining = _time_remaining
                                computed_detail.save()

                        if _time_remaining > zero_time:
                            self.demurrage = 0
                            self.despatch = round(
                                (_time_remaining / one_day) * self.despatch_rate,
                                2
                            )
                        else:
                            self.despatch = 0
                            self.demurrage = round(
                                (-_time_remaining / one_day) * self.demurrage_rate,
                                2
                            )
                        self.date_computed = now()
                        self.save(compute=True)

    def cargo_description_title(self):
        return self.cargo_description.lower().title()

    def csv(self):
        return mark_safe(
            '<a class="grp-button" '
            'href="/shipment/statement-csv/{}" '
            'target="_blank"'
            '>'
            'Download'
            '</a>'.format(self.shipment.name)
        )

    def PDF(self):
        return mark_safe(
            '<a class="grp-button" '
            'href="/shipment/statement/{}" '
            'target="_blank"'
            '>'
            'View'
            '</a>'.format(self.shipment.name)
        )

    def time_can_test(self):
        return self.can_test * \
            datetime.timedelta(minutes=5) * \
            float(self.can_test_factor)

    def time_limit(self):
        if self.tonnage:
            return round_second(
                (
                    datetime.timedelta(
                        days=self.tonnage / self.loading_terms
                    ) + self.time_can_test()
                ) or zero_time
            )
        return zero_time

    def vessel(self):
        if self.shipment.vessel:
            return self.shipment.vessel.name

    def clean(self):
        if hasattr(self, 'approvedlaydaysstatement'):
            if self.approvedlaydaysstatement.approved:
                raise ValidationError('Approved statement cannot be changed.')

        if self.arrival_tmc and self.arrival_pilot:
            if self.arrival_tmc < self.arrival_pilot:
                raise ValidationError(
                    'Arrival at TMC port should not be earlier than arrival at '
                    'Surigao Pilot Station.'
                )

        if self.arrival_tmc and self.nor_tender:
            if self.nor_tender < self.arrival_tmc:
                raise ValidationError(
                    'Tender of Notice of Readiness must not be earlier than '
                    'the arrival at TMC port.'
                )

        if self.nor_accepted and self.nor_tender:
            if self.nor_accepted < self.nor_tender:
                raise ValidationError('Acceptance of Notice of Readiness must '
                                      'be later than its tender.')

        if not self.shipment.vessel:
            raise ValidationError('Cannot save statement without vessel.')

    def save(self, compute=False, *args, **kwargs):
        if not compute:
            self.date_saved = now()
        super().save(*args, **kwargs)
        refresh_shipment_number()
        self.shipment.save()
        if not hasattr(self, 'approvedlaydaysstatement'):
            approval = ApprovedLayDaysStatement(statement=self, approved=False)
            approval.save()

    class Meta:
        ordering = [
            models.F('completed_loading').desc(nulls_last=False),
            models.F('nor_accepted').desc(nulls_last=False),
            models.F('nor_tender').desc(nulls_last=False),
            models.F('arrival_tmc').desc(nulls_last=False),
            models.F('arrival_pilot').desc(nulls_last=False)
        ]

    def __str__(self):
        return self.shipment.__str__()


class Product(Classification):
    moisture = models.DecimalField('%H₂O', max_digits=6, decimal_places=4, null=True, blank=True)
    ni = models.DecimalField('%Ni', max_digits=6, decimal_places=4, null=True, blank=True)
    fe = models.DecimalField('%Fe', max_digits=6, decimal_places=4, null=True, blank=True)


class Shipment(models.Model):
    """
    A shipment of nickel or iron ore.
    """
    name = NameField(max_length=10, unique=True)
    vessel = models.ForeignKey(
        'Vessel', null=True, blank=True, on_delete=models.PROTECT
    )
    destination = models.ForeignKey(
        Destination, null=True, blank=True, on_delete=models.PROTECT
    )
    buyer = models.ForeignKey(
        Buyer, null=True, blank=True, on_delete=models.SET_NULL
    )
    product = models.ForeignKey(
        Product, null=True, blank=True, on_delete=models.SET_NULL
    )
    spec_tonnage = models.PositiveIntegerField(
        help_text='Tonnage in sales contract.',
        null=True, blank=True
    )
    spec_moisture = models.DecimalField(
        '%H₂O Spec', max_digits=4, decimal_places=2, null=True, blank=True
    )
    spec_ni = models.DecimalField(
        '%Ni Spec', max_digits=4, decimal_places=2, null=True, blank=True
    )
    spec_fe = models.DecimalField(
        '%Fe Spec', max_digits=4, decimal_places=2, null=True, blank=True
    )
    target_tonnage = models.PositiveIntegerField(
        help_text='Determined during initial draft survey.',
        null=True, blank=True
    )
    dump_truck_trips = models.PositiveSmallIntegerField(null=True, blank=True)
    final_ni = models.DecimalField(
        '%Ni', max_digits=6, decimal_places=4, null=True, blank=True
    )
    final_fe = models.DecimalField(
        '%Fe', max_digits=6, decimal_places=4, null=True, blank=True
    )
    final_moisture = models.DecimalField(
        '%H₂O', max_digits=6, decimal_places=4, null=True, blank=True
    )
    base_price = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, help_text='US$'
    )
    final_price = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, help_text='US$'
    )
    boulders_tonnage = models.PositiveIntegerField(null=True, blank=True)
    boulders_processing_cost = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True, help_text='US$'
    )
    boulders_freight_cost = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True, help_text='US$'
    )
    demurrage = models.DecimalField(
        null=True, blank=True, max_digits=8, decimal_places=2,
        validators=[MinValueValidator(Decimal(0.00))]
    )
    despatch = models.DecimalField(
        null=True, blank=True, max_digits=8, decimal_places=2,
        validators=[MinValueValidator(Decimal(0.00))]
    )
    remarks = models.TextField(null=True, blank=True)

    def loading_period(self):
        if self.laydaysstatement:
            start = print_localzone(self.laydaysstatement.commenced_loading)
            end = print_localzone(self.laydaysstatement.completed_loading)
            if start and end:
                start_day = start.strftime('%-d')
                start_month = start.strftime('%B')
                start_year = start.strftime('%Y')
                end_day = end.strftime('%-d')
                end_month = end.strftime('%B')
                end_year = end.strftime('%Y')
                if start_year != end_year:
                    return f'{start_month} {start_day}, {start_year} - {end_month} {end_day}, {end_year}'.upper()
                elif start_month != end_month:
                    return f'{start_month} {start_day} - {end_month} {end_day}, {end_year}'.upper()
                else:
                    return f'{start_month} {start_day} - {end_day}, {end_year}'.upper()

    def name_html(self):
        if self.name.isdigit():
            return mark_safe(f'{self.name}<sup>{ordinal_suffix(self.name)}</sup>')
        return self.name

    def name_latex(self):
        if self.name.isdigit():
            return f'{self.name}$^\\mathrm{{\\text{{' + \
                f'{ordinal_suffix(self.name)}}}}}$'
        return self.name

    def clean(self):
        original_obj = Shipment.objects.filter(id=self.id)
        if original_obj.exists():
            original_obj = original_obj[0]

        if self.despatch and self.demurrage:
            if self.demurrage > 0 and self.despatch > 0:
                raise ValidationError(
                    'Demurrage and despatch cannot have values at the same time.'
                )

        if hasattr(self, 'shipmentloadingassay'):
            if hasattr(self.shipmentloadingassay, 'approvedshipmentloadingassay'):
                if self.shipmentloadingassay.approvedshipmentloadingassay.approved:
                    if self.destination != original_obj.destination:
                        raise ValidationError('Destination cannot be changed if assay is already approved.')
                    if self.product != original_obj.product:
                        raise ValidationError('Product cannot be changed if assay is already approved.')
                    if self.vessel != original_obj.vessel:
                        raise ValidationError('Vessel cannot be changed if assay is already approved.')

        if hasattr(self, 'laydaysstatement'):
            if hasattr(self.laydaysstatement, 'approvedlaydaysstatement'):
                if self.laydaysstatement.approvedlaydaysstatement.approved:
                    if self.demurrage != original_obj.demurrage:
                        raise ValidationError('Demurrage cannot be changed if laydays statement is already approved.')
                    if self.despatch != original_obj.despatch:
                        raise ValidationError('Despatch cannot be changed if laydays statement is already approved.')

    def save(self, refresh=True, *args, **kwargs):
        if self.product:
            if not self.spec_moisture:
                self.spec_moisture = self.product.moisture
            if not self.spec_ni:
                self.spec_ni = self.product.ni
            if not self.spec_fe:
                self.spec_fe = self.product.fe
        super().save(*args, **kwargs)
        if refresh:
            refresh_shipment_number()
            if self.vessel:
                for trip in self.vessel.trip_set.all():
                    trip.save()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(demurrage=0) | models.Q(despatch=0),
                name='dem_des_with_zero'
            )
        ]
        indexes = [models.Index(fields=['name'])]
        ordering = [
            models.F('laydaysstatement__completed_loading').desc(nulls_last=False),
            models.F('laydaysstatement__nor_accepted').desc(nulls_last=False),
            models.F('laydaysstatement__nor_tender').desc(nulls_last=False),
            models.F('laydaysstatement__arrival_tmc').desc(nulls_last=False),
            models.F('laydaysstatement__arrival_pilot').desc(nulls_last=False),
            models.F('name').desc()
        ]

    def __str__(self):
        if self.name.isdigit():
            return f'{self.name}{ordinal_suffix(self.name)}'
        return self.name


class ShipmentNumber(models.Model):
    """
    Materialized view.
    """
    shipment = models.OneToOneField(Shipment, on_delete=models.DO_NOTHING)
    number = models.CharField(max_length=10, unique=True)
    class Meta:
        managed = False
        db_table = 'shipment_number'


class Vessel(models.Model):
    """
    Bulk cargo vessel used for exporting nickel and iron ore.
    """
    name = MarineVesselName(max_length=50)
    stripped_name = AlphaNumeric(
        max_length=50, unique=True, null=True, blank=True
    )

    class Meta:
        ordering = ['name']

    def clean(self):
        stripped_name = sub(r'\s+', ' ', str(self.name).upper().strip())
        stripped_name = sub(r'^M[^a-zA-Z]*V\s*', '', stripped_name)
        stripped_name = sub(r'[^\w]', '', str(stripped_name))
        if Vessel.objects.all().exclude(id=self.id).filter(stripped_name = stripped_name).exists():
            raise ValidationError("Vessel name exists.")

    def save(self, *args, **kwargs):
        stripped_name = sub(r'\s+', ' ', str(self.name).upper().strip())
        stripped_name = sub(r'^M[^a-zA-Z]*V\s*', '', stripped_name)
        self.stripped_name = stripped_name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
