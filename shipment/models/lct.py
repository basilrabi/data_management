import datetime

from django.core.exceptions import ValidationError
from django.db import models

from custom.fields import NameField

class LCT(models.Model):
    """
    Landing craft tank. Used in transporting nickel and iron ore from the wharf
    to the Vessel.
    """
    name = NameField(max_length=50, unique=True)
    capacity = models.PositiveSmallIntegerField(help_text='Capacity in tons')

    class Meta:
        verbose_name = "LCT"
        verbose_name_plural = "LCT's"
        ordering = ['name']

    def __str__(self):
        return self.name

class LCTContract(models.Model):
    """
    Lease contract date (for rented LCT's) or service span (for in-house LCT's).
    """
    lct = models.ForeignKey('LCT', on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

    def clean(self):
        if self.end:
            if self.end < self.start:
                raise ValidationError('End of contract should not be earlier'
                                      ' than start of contract.')

        # pylint: disable=E1101
        if self.lct.lctcontract_set.filter(
            models.Q(
                start__lte=self.end or self.start + datetime.timedelta(300)
            ),
            models.Q(end__gte=self.start) | models.Q(end__isnull=True)
        ).exclude(id=self.id).count() > 0:
            raise ValidationError('Contract dates should not overlap')

    class Meta:
        verbose_name = 'LCT Contract'
        verbose_name_plural = 'LCT Contracts'
        ordering = ['lct', 'start']

    def __str__(self):
        # pylint: disable=E1101
        return  'Contract ' + str(self.id) + ': ' + self.lct.name

class Trip(models.Model):
    """
    A trip of the LCT. The trip starts when the LCT docks at the wharf and ends
    at the next docking at the wharf.
    """
    lct = models.ForeignKey('LCT', on_delete=models.CASCADE)
    vessel = models.ForeignKey('Vessel',
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True)

    STATUS_CHOICES = (
        ('rejected', 'Cargo Rejected by Vessel'),
        ('loaded', 'Cargo Loaded to Vessel'),
        ('partial', 'Cargo Partially Loaded to Vessel'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    dump_truck_trips = models.PositiveSmallIntegerField(default=0)
    vessel_grab = models.PositiveSmallIntegerField(default=0)
    interval_from = models.DateTimeField(null=True, blank=True)
    interval_to = models.DateTimeField(null=True, blank=True)
    valid = models.BooleanField(default=False,
                                help_text='A valid trip coincides with the '
                                          'shipment schedule.')

    def cycle(self):
        if self.interval_to:
            return self.interval_to - self.interval_from
        return datetime.timedelta(0)

    def _interval_from(self):
        # pylint: disable=E1101
        if self.tripdetail_set.all().count() > 0:
            return self.tripdetail_set.all() \
                .aggregate(models.Min('interval_from'))['interval_from__min']

    def _interval_to(self):
        # pylint: disable=E1101
        if self.tripdetail_set.all().count() > 1:
            return self.tripdetail_set.all() \
                .aggregate(models.Max('interval_from'))['interval_from__max']

    def _valid(self):
        """
        Checks whether the trip overlaps with the vessel's shipment.
        """
        if self.interval_to:
            # pylint: disable=E1101
            if self.vessel.shipment_set.filter(
                models.Q(start_loading__lte=self.interval_to),
                models.Q(end_loading__gte=self.interval_from) |
                models.Q(end_loading__isnull=True)
            ).count() > 0:
                return True
        return False

    def clean(self):
        if self.status != 'rejected':
            if self.dump_truck_trips < 1:
                raise ValidationError('Dump truck trips is required.')
            if self.vessel_grab < 1:
                raise ValidationError('Number of vessel grabs used required.')

    def save(self, *args, **kwargs):
        if self._interval_from():
            self.interval_from = self._interval_from()
        self.interval_to = self._interval_to()
        self.valid = self._valid()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['lct', '-interval_from']

    def __str__(self):
        # pylint: disable=E1101
        return 'Record: ' + str(self.id) + ', LCT: ' + self.lct.name

class TripDetail(models.Model):
    """
    An interval within the LCT Trip. This is equivalent to one row in the
    statement of facts of the LCT.
    """
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE)
    interval_from = models.DateTimeField()

    CLASS_CHOICES = (
        ('preparation_loading', 'Preparation for Loading'),
        ('loading', 'Loading'),
        ('preparation_departure', 'Preparation for Departure'),
        ('travel_to_vessel', 'Travel to Vessel'),
        ('preparation_unloading', 'Preparation for Unloading'),
        ('unloading', 'Unloading'),
        ('preparation_castoff', 'Preparation for Castoff'),
        ('travel_to_wharf', 'Travel to Wharf'),
        ('waiting_for_cargo', 'Wating for Cargo'),
        ('waiting_for_dock', 'Waiting for Available Dock'),
        ('waiting_for_tide', 'Waiting for Safe Water Level'),
        ('waiting_for_vessel', 'Waiting for Vessel'),
        ('swell', 'Swell'),
        ('rain', 'Rain'),
        ('rain_swell', 'Rain and Swell'),
        ('refueling', 'Refueling'),
        ('rewatering', 'Rewatering'),
        ('end', 'End'),
    )

    interval_class = models.CharField(max_length=30, choices=CLASS_CHOICES)
    remarks = models.TextField(null=True, blank=True)

    def interval_to(self):
        if self.next():
            return self.next().interval_from

    def next(self):
        # pylint: disable=E1101
        return self.trip.tripdetail_set.filter(models.Q(
            interval_from__gt=self.interval_from
        )).order_by('interval_from').first()

    class Meta:
        ordering = ['interval_from']

    def clean(self):
        # pylint: disable=E1101
        if self.trip.tripdetail_set.filter(interval_from=self.interval_from) \
                .exclude(id=self.id).count() > 0:
            raise ValidationError('Times should be different.')

        if self.trip.tripdetail_set.filter(interval_class='end') \
                .exclude(id=self.id).count() > 0:
            raise ValidationError('Only one end is allowed.')

        for trip in self.trip.lct.trip_set.all().exclude(id=self.trip.id):
            if trip._interval_to():
                if trip._interval_from() < self.interval_from and \
                        trip._interval_to() > self.interval_from:
                    raise ValidationError('Travel time of one LCT should not'
                                          ' overlap.')

        if self.trip.lct.lctcontract_set.filter(
            models.Q(start__lte=self.interval_from.date()),
            models.Q(end__gte=self.interval_from.date()) |
            models.Q(end__isnull=True)
        ).count() < 1:
            raise ValidationError('LCT used is not rented or has no lease'
                                  ' contract for the date inputed.')

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.trip.save() # pylint: disable=E1101

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.trip.save() # pylint: disable=E1101
