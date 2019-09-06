import datetime

from django.core.exceptions import ValidationError
from django.db import models

from custom.fields import NameField

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

    class Meta:
        ordering = ['-start_loading', 'name']

    def __str__(self):
        return self.name

class Vessel(models.Model):
    """
    Bulk cargo vessel used for exporting nickel and iron ore.
    """
    name = NameField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
