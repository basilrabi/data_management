import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.html import mark_safe
from django.utils.timezone import now

from custom.fields import (AlphaNumeric,
                           NameField,
                           MarineVesselName,
                           ordinal_suffix,
                           round_second,
                           round_up_day,
                           to_dhms,
                           to_hm,
                           to_hms)
from custom.variables import one_day, zero_time

# pylint: disable=no-member

class LayDaysDetail(models.Model):
    """
    An entry in the laydays statement.
    """
    laydays = models.ForeignKey('LayDaysStatement', on_delete=models.CASCADE)
    interval_from = models.DateTimeField()
    loading_rate = models.PositiveSmallIntegerField(
        help_text='Percent available vessel grabs.'
    )

    CLASS_CHOICES = (
        ('continuous loading', 'Continuous Loading'),
        ('sun drying', 'Sun Drying'),
        ('heavy swell', 'Heavy Swell'),
        ('rain', 'Rain'),
        ('rain and heavy swell', 'Rain and Heavy Swell'),
        ('waiting for cargo', 'Waiting for Cargo'),
        ('waiting for cargo due to rejection', 'Waiting for Cargo (rejected)'),
        ('end', 'End'),
        ('vessel arrived behind of schedule', 'Vessel Arrived Behind of Schedule'),
        ('others', '-')
    )

    interval_class = models.CharField(max_length=50, choices=CLASS_CHOICES)
    remarks = models.TextField(null=True, blank=True)
    can_test = models.BooleanField(
        default=False,
        help_text='Can test was conducted in this interval.'
    )

    def interval(self):
        if self.next():
            return self.next().interval_from - self.interval_from

    def next(self):
        return self.laydays.laydaysdetail_set.filter(models.Q(
            interval_from__gt=self.interval_from
        )).order_by('interval_from').first()

    class Meta:
        ordering = ['interval_from']

    def clean(self):
        if self.laydays.laydaysdetail_set \
                .filter(interval_from=self.interval_from) \
                .exclude(id=self.id).count() > 0:
            raise ValidationError('Times should be unique.')

        if self.interval_class == 'end' and self.laydays.laydaysdetail_set \
                .filter(interval_class='end') \
                .exclude(id=self.id).count() > 0:
            raise ValidationError('Only one end is allowed.')

        if (self.loading_rate or 0) > 100:
            raise ValidationError("The limit of loading rate is 100.")

class LayDaysDetailComputed(models.Model):

    laydays = models.ForeignKey('LayDaysStatement', on_delete=models.CASCADE)
    interval_from = models.DateTimeField()
    loading_rate = models.PositiveSmallIntegerField(
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
                self.interval() * (self.previous().loading_rate / 100)
            )
        return zero_time

    def consumed_formated(self):
        """
        Laytime consumption formatted in hours:minutes:seconds
        """
        return to_hms(self.consumed())

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

    def _clean(self):
        """
        Removes redundant details.
        """
        final = False
        while not final:
            for detail in self.laydaysdetail_set.all():
                if not detail.next():
                    final = True
                    break

                if detail.loading_rate == detail.next().loading_rate and \
                        detail.interval_class == detail.next().interval_class and \
                        detail.remarks == detail.next().remarks and \
                        detail.can_test == detail.next().can_test:
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
                    if loading_details.first().can_test:
                        self.commenced_loading += datetime.timedelta(minutes=5)

                    end_details = self.laydaysdetail_set .filter(interval_class='end')
                    #  Proceed computation if end of statement exists
                    if end_details.exists():

                        # Record end of loading operation
                        self.completed_loading = loading_details.last().next().interval_from

                        # Update shipment data with the update of laytime statement
                        if self.shipment.end_loading != self.completed_loading or self.shipment.start_loading != self.commenced_loading:
                            self.shipment.start_loading = self.commenced_loading
                            self.shipment.end_loading = self.completed_loading
                            self.shipment.save()

                        _time_remaining = self.time_limit() + self.additional_laytime
                        self.time_allowed = _time_remaining
                        for detail in self.laydaysdetail_set.all():

                            # Create initial computated detail object copied from the orignal detail
                            computed_detail = LayDaysDetailComputed(
                                laydays=detail.laydays,
                                interval_from=detail.interval_from,
                                loading_rate=detail.loading_rate,
                                interval_class=detail.interval_class,
                                remarks=detail.remarks
                            )
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
                                            loading_rate=previous_detail.loading_rate,
                                            interval_class=previous_detail.interval_class
                                        )
                                        time_remaining = _time_remaining - computed_detail_virtual.consumed()

                                        # During lay time expiry while using virtual time stamp, save a time stamp at the end of allowed laytime.
                                        if _time_remaining > zero_time and time_remaining < zero_time:
                                            computed_detail_virtual.interval_from = previous_detail.interval_from + (
                                                round_second(
                                                    _time_remaining / (computed_detail_virtual.previous().loading_rate / 100)
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
                                                    _time_remaining / (previous_detail.loading_rate / 100)
                                                )
                                            ),
                                            loading_rate=previous_detail.loading_rate,
                                            interval_class=previous_detail.interval_class,
                                            remarks='laytime expires',
                                            time_remaining=zero_time
                                        )
                                        computed_detail_virtual.save()
                                        _time_remaining = zero_time

                                # If the previous time interval does not cross midnight, save the present detail as new computed detail.
                                time_remaining = _time_remaining - computed_detail.consumed()

                                # During lay time expiry, save a time stamp at the end of allowed laytime.
                                if _time_remaining > zero_time and time_remaining < zero_time:
                                    computed_detail_virtual = LayDaysDetailComputed(
                                        laydays=detail.laydays,
                                        interval_from=previous_detail.interval_from + round_second(_time_remaining / previous_detail.loading_rate),
                                        loading_rate=previous_detail.loading_rate,
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

    def PDF(self):
        return mark_safe(
            '<a class="grp-button" '
            'href="/shipment/statement/{}" '
            'target="_blank"'
            '>'
            'Compute and View Statement'
            '</a>'.format(self.__str__())
        )

    def shipment_name_latex(self):
        if self.shipment.name.isdigit():
            return f'{self.shipment.name}$^\\mathrm{{\\text{{' + \
                f'{ordinal_suffix(self.shipment.name)}}}}}$'
        return self.shipment.name

    def time_can_test(self):
        return self.can_test * datetime.timedelta(minutes=2.5)

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
        return self.shipment.vessel.name

    def clean(self):
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

    def save(self, compute=False, *args, **kwargs):
        if self.tonnage:
            if self.tonnage != self.shipment.tonnage:
                self.shipment.tonnage = self.tonnage
                self.shipment.save()
        if not compute:
            self.date_saved = now()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-completed_loading']

    def __str__(self):
        return self.shipment.name

class Shipment(models.Model):
    """
    A shipment of nickel or iron ore.
    """
    name = NameField(max_length=10, unique=True)
    vessel = models.ForeignKey('Vessel', on_delete=models.CASCADE)
    start_loading = models.DateTimeField()
    end_loading = models.DateTimeField(null=True, blank=True)
    dump_truck_trips = models.PositiveSmallIntegerField(default=0)
    tonnage = models.PositiveIntegerField(default=0)

    def clean(self):
        if self.end_loading:
            if self.end_loading < self.start_loading:
                raise ValidationError(
                    'End of loading should not be earlier than start of loading'
                )

        if self.vessel.shipment_set.filter(
            models.Q(
                start_loading__lte=self.end_loading or
                    self.start_loading + datetime.timedelta(30)
            ),
            models.Q(end_loading__gte=self.start_loading) |
            models.Q(end_loading__isnull=True)
        ).exclude(id=self.id).count() > 0:
            raise ValidationError('Vessel trip should not overlap.')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for trip in self.vessel.trip_set.all():
            trip.save()

    class Meta:
        ordering = ['-start_loading', 'name']

    def __str__(self):
        return self.name

class Vessel(models.Model):
    """
    Bulk cargo vessel used for exporting nickel and iron ore.
    """
    name = MarineVesselName(max_length=50)
    stripped_name = AlphaNumeric(
        max_length=50, unique=True, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        self.stripped_name = self.name
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
