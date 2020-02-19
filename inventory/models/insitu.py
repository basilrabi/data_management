from django.contrib.gis.db import models
from location.models.source import Cluster

class Block(models.Model):
    """
    A rectangular cuboid representing a volume of in-situ material with
    an assumed uniform chemical and physical characteristics.
    """
    name = models.CharField(max_length=20)
    z = models.SmallIntegerField()
    ni = models.FloatField()
    fe = models.FloatField()
    co = models.FloatField()
    excavated = models.BooleanField(default=False)
    cluster = models.ForeignKey(
        Cluster, null=True, blank=True, on_delete=models.PROTECT
    )
    geom = models.PointField(srid=3125)

    class Meta:
        indexes = [
            models.Index(fields=['z', 'ni'])
        ]

    def __str__(self):
        return self.name
