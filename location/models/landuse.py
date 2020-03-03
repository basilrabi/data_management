from django.contrib.gis.db import models

class RoadArea(models.Model):
    """
    Area of land covered by roads.
    """
    date_surveyed = models.DateField(unique=True)
    geom = models.MultiPolygonField(srid=3125, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['date_surveyed'])
        ]

    def __str__(self):
        return str(self.date_surveyed)
