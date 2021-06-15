from django.contrib.gis.db.models import (
    CASCADE,
    CheckConstraint,
    DateTimeField,
    DecimalField,
    ForeignKey,
    Model,
    PointField,
    PositiveSmallIntegerField,
    Q
)
from django.db.models import constraints

from shipment.models.dso import LayDaysStatement


class Anchorage(Model):
    """
    Anchorage location of a vessel during a running lay time.
    """
    laydays = ForeignKey(LayDaysStatement, on_delete=CASCADE)
    anchored = DateTimeField()
    latitude_degree = PositiveSmallIntegerField(default=9)
    latitude_minutes = DecimalField(max_digits=7, decimal_places=5)
    longitude_degree = PositiveSmallIntegerField(default=125)
    longitude_minutes = DecimalField(max_digits=7, decimal_places=5)
    geom = PointField(srid=4326, null=True)

    class Meta:
        constraints = [
            CheckConstraint(check=Q(latitude_minutes__gte=0), name='lat_floor'),
            CheckConstraint(check=Q(latitude_minutes__lt=60), name='lat_ceiling'),
            CheckConstraint(check=Q(longitude_minutes__gte=0), name='lon_floor'),
            CheckConstraint(check=Q(longitude_minutes__lt=60), name='lon_ceiling')
        ]
        ordering = ['anchored']

    def __str__(self):
        if self.laydays:
            return self.laydays.vessel()
