from django.contrib.gis.db import models

from custom.fields import MineBlockField, NameField, PileField
from .landuse import RoadArea

# pylint: disable=no-member

RIDGES = (
    ('HY', 'Hayanggabon'),
    ('T1', 'Taga 1'),
    ('T2', 'Taga 2'),
    ('T3', 'Taga 3'),
    ('UR', 'Urbiztondo'),
    ('KB', 'Kinalablaban')
)

class Cluster(models.Model):
    """
    A group of adjacent `inventory.Blocks` with the same elevation at the same
    mine block.
    """
    name = models.CharField(max_length=30)
    z = models.SmallIntegerField(default=0)
    count = models.IntegerField(
        null=True,
        blank=True,
        help_text='A unique number for the cluster at the same grade classification and at the same mine block.'
    )
    ore_class = models.CharField(max_length=1, null=True, blank=True)
    mine_block = models.CharField(max_length=20, null=True, blank=True)
    ni = models.FloatField(default=0)
    fe = models.FloatField(default=0)
    co = models.FloatField(default=0)
    distance_from_road = models.FloatField(default=0)
    road = models.ForeignKey(
        RoadArea,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        help_text='Road used to adjust the cluster geometry.'
    )
    with_layout = models.BooleanField(default=False)
    date_scheduled = models.DateField(
        null=True,
        blank=True,
        help_text='Scheduled date of start of excavation'
    )
    excavated = models.BooleanField(default=False)
    geom = models.MultiPolygonField(srid=3125, null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(distance_from_road__gte=0),
                                   name='non_negative_distance'),
            models.UniqueConstraint(fields=['count', 'ore_class', 'mine_block'],
                                    name='unique_cluster_name')
        ]
        indexes = [models.Index(fields=['z'])]
        ordering = ['-date_scheduled', 'ore_class', 'name']

    def feature_as_str(self):
        """
        String file representation of the feature.
        """
        if self.geom:
            feature_str = ''
            for polygon in self.geom.coords:
                for shape in polygon:
                    for coords in shape:
                        feature_str += f'{self.id}, {coords[1]}, {coords[0]}, {self.z-3}, {self.name}, {self.ore_class}, {self.mine_block}, {self.ni}, {self.fe}, {self.co}\n'
                    feature_str += '0, 0, 0, 0,\n'
            return feature_str

    def __str__(self):
        return self.name

class DrillHole(models.Model):
    """
    Drill hole collar technical descriptions.
    """
    name = NameField(max_length=20, unique=True)
    date_drilled = models.DateField(null=True, blank=True)
    local_block = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text='block location in local coordinates'
    )
    local_easting = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text='collar x-coordinates in local grid'
    )
    local_northing = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text='collar y-coordinates in local grid'
    )
    local_z = models.FloatField(
        null=True,
        blank=True,
        help_text='collar elevation prior to the use of SRID:3125'
    )
    x = models.FloatField(
        null=True, blank=True, help_text='collar x-coordinates in SRID:3125'
    )
    y = models.FloatField(
        null=True, blank=True, help_text='collar y-coordinates in SRID:3125'
    )
    z = models.FloatField(null=True, blank=True, help_text='collar elevation')
    z_present = models.FloatField(
        null=True, blank=True, help_text='present ground elevation'
    )
    geom = models.PointField(srid=3125, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class MineBlock(models.Model):
    name = MineBlockField(max_length=20, unique=True)
    ridge = models.CharField(max_length=2, choices=RIDGES)
    geom = models.PolygonField(srid=3125, null=True, blank=True)

    class Meta:
        ordering = ['ridge', 'name']

    def __str__(self):
        return f'{self.ridge} MB {self.name}'

class Stockyard(models.Model):
    name = PileField(max_length=20, unique=True)
    geom = models.MultiPolygonField(srid=3125, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'
