import datetime

from django.core.exceptions import ValidationError
from django.db import models

from custom.fields import AlphaNumeric, NameField, MarineVesselName
from custom.variables import day_time, zero_time

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
        ('can_test', 'Can Test'),
        ('end', 'End'),
        ('loading', 'Continuous Loading'),
        ('others', '-'),
        ('sun_dry', 'Cargo Sun Drying'),
        ('swell', 'Heavy Swell'),
        ('rain', 'Rain'),
        ('rain_swell', 'Rain and Swell'),
        ('waiting_for_cargo', 'Waiting for Cargo')
    )

    interval_class = models.CharField(max_length=30, choices=CLASS_CHOICES)
    remarks = models.TextField(null=True, blank=True)

    def interval(self):
        if self.next():
            return self.next().interval_from - self.interval_from

    def next(self):
        # pylint: disable=E1101
        return self.laydays.laydaysdetail_set.filter(models.Q(
            interval_from__gt=self.interval_from
        )).order_by('interval_from').first()

    def running(self):
        RUNNING_CLASS = ['loading', 'sun_dry', 'waiting_for_cargo']
        if self.interval_class in RUNNING_CLASS:
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

        if self.loading_rate > 100:
            raise ValidationError("The limit of loading rate is 100.")

class LayDaysStatement(models.Model):
    """
    A vessel's laydays statement for a shipment loading.
    """
    shipment = models.OneToOneField('Shipment', on_delete=models.CASCADE)
    vessel_voyage = models.CharField(max_length=20, null=True, blank=True)
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
    loading_terms = models.PositiveSmallIntegerField(default=6000)
    demurrage_rate = models.PositiveSmallIntegerField(default=11000)
    despatch_rate = models.PositiveSmallIntegerField(default=5500)
    can_test = models.PositiveSmallIntegerField(
        default=0,
        help_text='Number of can tests performed.'
    )
    time_allowed = models.DecimalField(
        default=0, max_digits=7, decimal_places=5
    )
    time_used = models.DecimalField(
        default=0, max_digits=7, decimal_places=5
    )
    demurrage = models.DecimalField(
        default=0, max_digits=8, decimal_places=2
    )
    despatch = models.DecimalField(
        default=0, max_digits=8, decimal_places=2
    )

    def laytime_difference(self):
        return round(self.time_allowed - self.time_used, 5)

    def time_can_test(self):
        return self.can_test / 576

    def time_limit(self):
        if self.tonnage:
            return (
                (
                    (self.tonnage / self.loading_terms) + self.time_can_test()
                ) or 0
            )
        else:
            return 0

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
        n_details = self.laydaysdetail_set.all().count()
        if n_details >= 1:
            self.commenced_laytime = self.laydaysdetail_set.first() \
                .interval_from
            self.commenced_loading = self.laydaysdetail_set \
                .filter(interval_class='loading').first().interval_from
            if n_details >= 2:
                self.completed_loading = self.laydaysdetail_set.last() \
                    .interval_from
                self.time_used = (
                    self.completed_loading - self.commenced_loading
                ) / day_time
                self.shipment.end_loading = self.completed_loading
            self.shipment.start_loading = self.commenced_loading
        if self.tonnage:
            self.shipment.tonnage = self.tonnage
        self.shipment.save()

        _time_allowed = zero_time
        _time_limit = datetime.timedelta(self.time_limit())

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

        self.time_allowed = _time_allowed / day_time
        _laytime_difference = self.laytime_difference()
        if _laytime_difference > 0:
            self.demurrage = 0
            self.despatch = round(
                _laytime_difference * self.despatch_rate, 2
            )
        else:
            self.despatch = 0
            self.demurrage = round(
                _laytime_difference * self.demurrage_rate, 2
            )
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
