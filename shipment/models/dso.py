import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.html import mark_safe

from custom.fields import AlphaNumeric, NameField, MarineVesselName
from custom.variables import one_day, one_hour, one_minute, zero_time

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
        ('can test', 'Can Test'),
        ('others', '-')
    )

    interval_class = models.CharField(max_length=50, choices=CLASS_CHOICES)
    remarks = models.TextField(null=True, blank=True)
    pause_override = models.BooleanField(
        default=False,
        help_text='Exclude this detail as running lay time.'
    )

    def interval(self):
        if self.next():
            return self.next().interval_from - self.interval_from

    def interval_formated(self):
        """
        Time interval formatted in hours:minutes
        """
        if self.interval():
            value = self.interval()
            hours = value // one_hour
            minutes = (value - (hours * one_hour)) // one_minute
            return f'{hours:02d}:{minutes:02d}'

    def next(self):
        # pylint: disable=E1101
        return self.laydays.laydaysdetail_set.filter(models.Q(
            interval_from__gt=self.interval_from
        )).order_by('interval_from').first()

    def running(self):
        """
        Is the detail interval consuming lay time?
        """
        RUNNING_CLASS = [
            'continuous loading',
            'sun drying',
            'waiting for cargo',
            'waiting for cargo due to rejection',
            'others'
        ]
        if self.interval_class in RUNNING_CLASS and not self.pause_override:
            return True
        return False

    class Meta:
        ordering = ['interval_from']

    def clean(self):
        # pylint: disable=E1101
        if self.laydays.laydaysdetail_set \
                .filter(interval_from=self.interval_from) \
                .exclude(id=self.id).count() > 0:
            raise ValidationError('Times should be unique.')

        if self.laydays.laydaysdetail_set \
                .filter(interval_class='end') \
                .exclude(id=self.id).count() > 0:
            raise ValidationError('Only one end is allowed.')

        if (self.loading_rate or 0) > 100:
            raise ValidationError("The limit of loading rate is 100.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.laydays.save() # pylint: disable=no-member

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
    time_used = models.DurationField(default=zero_time)
    demurrage = models.DecimalField(
        default=0, max_digits=8, decimal_places=2
    )
    despatch = models.DecimalField(
        default=0, max_digits=8, decimal_places=2
    )
    date_saved = models.DateField(null=True, blank=True)
    report_date = models.DateField(
        null=True,
        blank=True,
        help_text='Date of statement. Defaults to date_saved.'
    )
    revised = models.BooleanField(
        default=False,
        help_text='This lay days statement is revised from a previous version.'
    )

    def cargo_description_title(self):
        # pylint: disable=no-member
        return self.cargo_description.lower().title()

    def laytime_difference(self):
        return self.time_allowed - self.time_used

    def PDF(self):
        return mark_safe(
            '<a class="grp-button" '
            'href="/shipment/statement/{}" '
            'target="_blank"'
            '>'
            'View Statement'
            '</a>'.format(self.__str__())
        )

    def time_can_test(self):
        return self.can_test * datetime.timedelta(minutes=2.5)

    def time_limit(self):
        if self.tonnage:
            return (
                (
                    datetime.timedelta(
                        days=self.tonnage / self.loading_terms
                    ) + self.time_can_test()
                ) or zero_time
            )
        else:
            return zero_time

    def vessel(self):
        # pylint: disable=E1101
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

    def save(self, *args, **kwargs):
        # pylint: disable=E1101

        # Copy shipment period
        if self.laydaysdetail_set.all().count() >= 1:
            commenced_laytime = self.laydaysdetail_set.first()
            last_detail = self.laydaysdetail_set.last()
            self.commenced_laytime = commenced_laytime.interval_from
            commenced_loading = self.laydaysdetail_set \
                .filter(interval_class='continuous loading').first()
            if commenced_loading:
                self.commenced_loading = commenced_loading.interval_from
                self.shipment.start_loading = self.commenced_loading
                try:
                    end_laytime = self.laydaysdetail_set \
                        .get(interval_class='end')
                except:
                    end_laytime = None
                if end_laytime:
                    self.completed_loading = end_laytime.interval_from
                    if self.shipment.end_loading != self.completed_loading:
                        self.shipment.end_loading = self.completed_loading
                        self.shipment.save()

            self.time_used = last_detail.interval_from - self.commenced_laytime

            _time_allowed = zero_time
            _time_limit = self.time_limit()

            for detail in self.laydaysdetail_set.all():
                if not detail.next():
                    break

                detail_interval = detail.interval()
                load_factor = detail.loading_rate / 100
                if _time_limit > zero_time:
                    if detail.running():
                        apparent_interval = detail_interval * load_factor
                        if _time_limit >= apparent_interval:
                            _time_limit -= apparent_interval
                            _time_allowed += detail_interval
                        else:
                            _time_allowed += _time_limit / load_factor
                            _time_limit = zero_time
                    else:
                        _time_allowed += detail_interval
                else:
                    break

            if _time_limit > zero_time:
                _time_allowed += _time_limit

            self.time_allowed = _time_allowed
            _laytime_difference = self.laytime_difference()
            if _laytime_difference > zero_time:
                self.demurrage = 0
                self.despatch = round(
                    (_laytime_difference / one_day) * self.despatch_rate, 2
                )
            else:
                self.despatch = 0
                self.demurrage = round(
                    (_laytime_difference / one_day) * self.demurrage_rate, 2
                )

        if self.tonnage:
            if self.tonnage != self.shipment.tonnage:
                self.shipment.tonnage = self.tonnage
                self.shipment.save()

        self.date_saved = datetime.date.today()
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
        # pylint: disable=E1101
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
        # pylint: disable=E1101
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
