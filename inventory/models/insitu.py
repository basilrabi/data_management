from django.contrib.gis.db import models
from location.models.source import Cluster, DrillHole

class Block(models.Model):
    """
    A rectangular prism representing a volume of in-situ material with
    an assumed uniform chemical and physical characteristics. The present
    dimensions used are:
    10 meter length along x (Easting)
    10 meter length along y (Northing)
    3 meter length along z (Elevation)
    However, geometry is only saved as a 2-dimensional square in the database.
    """
    name = models.CharField(max_length=20)
    z = models.SmallIntegerField(
        help_text='Elevation of the top face of the block.'
    )
    ni = models.FloatField(
        help_text='Estimated nickel content of the block in percent.'
    )
    fe = models.FloatField(
        help_text='Estimated iron content of the block in percent.'
    )
    co = models.FloatField(
        help_text='Estimated cobalt content of the block in percent.'
    )
    cluster = models.ForeignKey(
        Cluster, null=True, blank=True, on_delete=models.PROTECT
    )
    depth = models.FloatField(
        null=True,
        blank=True,
        help_text='''Distance of the centroid from the surface. A positive
        value means that the centroid is still below the surface.
        '''
    )
    planned_excavation_date = models.DateField(null=True, blank=True)
    exposed = models.BooleanField(null=True, blank=True)
    geom = models.PointField(srid=3125)

    class Meta:
        indexes = [
            models.Index(fields=['z']),
            models.Index(fields=['exposed', 'z', 'planned_excavation_date'])
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
