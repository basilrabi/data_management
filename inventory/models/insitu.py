from django.contrib.gis.db import models
from location.models.source import Cluster, DrillHole

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

class DrillArea(models.Model):
    """
    Area of influence of a drill hole.
    """
    drill_hole = models.OneToOneField(DrillHole, on_delete=models.PROTECT)
    factor = models.DecimalField(
        default=1,max_digits=5, decimal_places=4, null=True, blank=True
    )
    influence = models.PolygonField(srid=3125, null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(factor__lte=1), name='factor_max_drill_aoi'),
            models.CheckConstraint(check=models.Q(factor__gte=0), name='factor_min_drill_aoi')
        ]

    def __str__(self):
        return self.drill_hole.name
