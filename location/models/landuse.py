from django.contrib.gis.db.models import (
    DateField,
    ForeignKey,
    Index,
    Model,
    MultiPolygonField,
    SET_NULL
)

from custom.models import Classification, GeoClassification


class MPSA(GeoClassification):
    class Meta:
        verbose_name = 'Mineral Production Sharing Agreement'


class FacilityClassification(Classification):
    pass


class Facility(GeoClassification):
    classification = ForeignKey(
        FacilityClassification, null=True, blank=True, on_delete=SET_NULL
    )

    class Meta:
        verbose_name_plural = 'Facilities'


class FLA(GeoClassification):
    class Meta:
        verbose_name = 'Foreshore Lease Agreeement'


class PEZA(GeoClassification):
    class Meta:
        verbose_name = 'Philippine Economic Zone Authority Area'


class RoadArea(Model):
    """
    Area of land covered by roads.
    """
    date_surveyed = DateField(unique=True)
    geom = MultiPolygonField(srid=3125, null=True, blank=True)

    class Meta:
        indexes = [Index(fields=['date_surveyed'])]

    def __str__(self):
        return str(self.date_surveyed)


class WaterBody(GeoClassification):
    class Meta:
        verbose_name_plural = 'Water Bodies'
