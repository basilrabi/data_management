from django.contrib.gis.db.models import (
    BooleanField,
    CharField,
    CheckConstraint,
    DateField,
    DecimalField,
    FloatField,
    ForeignKey,
    Index,
    Model,
    OneToOneField,
    PROTECT,
    PointField,
    PolygonField,
    Q,
    SmallIntegerField
)
from location.models.source import Cluster, DrillHole


class Block(Model):
    """
    A rectangular prism representing a volume of in-situ material with
    an assumed uniform chemical and physical characteristics. The present
    dimensions used are:
    10 meter length along x (Easting)
    10 meter length along y (Northing)
    3 meter length along z (Elevation)
    However, geometry is only saved as a 2-dimensional square in the database.
    """
    name = CharField(max_length=20, unique=True)
    z = SmallIntegerField(help_text='Elevation of the top face of the block.')
    ni = FloatField(help_text='Estimated nickel content of the block in percent.')
    fe = FloatField(help_text='Estimated iron content of the block in percent.')
    co =FloatField(help_text='Estimated cobalt content of the block in percent.')
    cluster = ForeignKey(Cluster, null=True, blank=True, on_delete=PROTECT)
    depth = FloatField(
        null=True,
        blank=True,
        help_text='''Distance of the centroid from the surface. A positive
        value means that the centroid is still below the surface.
        '''
    )
    planned_excavation_date = DateField(null=True, blank=True)
    exposed = BooleanField(null=True, blank=True)
    geom = PointField(srid=3125)

    class Meta:
        indexes = [
            Index(fields=['z']),
            Index(fields=['exposed', 'z', 'planned_excavation_date']),
            Index(fields=['exposed', 'fe', 'ni', 'z', 'planned_excavation_date'])
        ]

    def __str__(self):
        return self.name


class DrillArea(Model):
    """
    Area of influence of a drill hole.
    """
    drill_hole = OneToOneField(DrillHole, on_delete=PROTECT)
    factor = DecimalField(
        default=1,max_digits=5, decimal_places=4, null=True, blank=True
    )
    influence = PolygonField(srid=3125, null=True, blank=True)

    class Meta:
        constraints = [
            CheckConstraint(check=Q(factor__lte=1), name='factor_max_drill_aoi'),
            CheckConstraint(check=Q(factor__gte=0), name='factor_min_drill_aoi')
        ]

    def __str__(self):
        return self.drill_hole.name
