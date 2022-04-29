from django.contrib.gis.db.models import (
    BooleanField,
    CharField,
    CheckConstraint,
    DateField,
    DateTimeField,
    FloatField,
    ForeignKey,
    Index,
    IntegerField,
    LineStringField,
    Model,
    MultiPolygonField,
    PROTECT,
    PointField,
    PolygonField,
    PositiveSmallIntegerField,
    Q,
    UniqueConstraint,
    SmallIntegerField
)
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields.related import OneToOneField

from custom.fields import MineBlockField, NameField
from custom.variables import ACI
from .landuse import RoadArea

RIDGES = (
    ('HY', 'Hayanggabon'),
    ('T1', 'Taga 1'),
    ('T2', 'Taga 2'),
    ('T3', 'Taga 3'),
    ('UR', 'Urbiztondo'),
    ('KB', 'Kinalablaban')
)


class BaseCluster(Model):
    """
    A group of adjacent `inventory.Blocks` with the same elevation at the same
    mine block.
    """
    date_scheduled = DateField(
        null=True,
        blank=True,
        help_text='''Date when the cluster is to be excavated.
        When this date is set, the geometry cannot be changed.'''
    )
    excavated = BooleanField(default=False)
    latest_layout_date = DateField(
        null=True,
        blank=True,
        help_text='''Latest date when the cluster is laid out on the field.
        This field is auto-generated based on ClusterLayout.'''
    )
    mine_block = CharField(max_length=20, null=True, blank=True)
    modified = DateTimeField()
    name = CharField(max_length=30)
    ore_class = CharField(max_length=1, null=True, blank=True)
    z = SmallIntegerField(default=0)

    co = FloatField(default=0)
    fe = FloatField(default=0)
    ni = FloatField(default=0)

    geom = MultiPolygonField(srid=3125, null=True, blank=True)

    class Meta:
        abstract = True

    def feature_as_str(self):
        """
        String file representation of the feature.
        """
        if self.geom:
            feature_str = ''
            for polygon in self.geom.coords:
                for shape in polygon:
                    for coords in shape:
                        feature_str += f'{self.id}, {coords[1]}, {coords[0]}, {self.z-3}, {self.name}, {self.ore_class}, {self.mine_block}, {self.ni}, {self.fe}, {self.co}, {self.date_scheduled or ""}, {self.latest_layout_date or ""}, {(self.geom.area * 3 * 1.5) or 0}\n'
                    feature_str += '0, 0, 0, 0,\n'
            return feature_str

    def getACI(self):
        return ACI[self.ore_class]

    def __str__(self):
        return self.name


class ClippedCluster(BaseCluster):
    """
    Cluster clipped using Crest. Majority of the fields come from Cluster
    while data updates are purely based on triggers.
    """
    cluster = OneToOneField('Cluster', on_delete=CASCADE)

    class Meta:
        indexes = [
            Index(fields=['z']),
            Index(fields=['mine_block', 'z'])
        ]


class Cluster(BaseCluster):
    """
    Created by grade control.
    """
    count = IntegerField(
        null=True,
        blank=True,
        help_text='A unique number for the cluster at the same grade classification and at the same mine block.'
    )
    distance_from_road = FloatField(default=0)
    road = ForeignKey(
        RoadArea,
        null=True,
        blank=True,
        on_delete=PROTECT,
        help_text='Road used to adjust the cluster geometry.'
    )
    dumping_area = ForeignKey(
        'Stockpile',
        null=True,
        blank=True,
        on_delete=PROTECT,
        help_text='Assigned dumping area.'
    )
    excavation_rate = IntegerField(
        null=True,
        blank=True,
        help_text='Percentage of blocks excavated.'
    )
    exposure_rate = IntegerField(
        null=True,
        blank=True,
        help_text='Percentage of blocks either exposed or excavated.'
    )

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(distance_from_road__gte=0),
                name='non_negative_distance'
            ),
            UniqueConstraint(
                fields=['count', 'ore_class', 'mine_block'],
                name='unique_cluster_name'
            )
        ]
        indexes = [
            Index(fields=['z']),
            Index(fields=['mine_block', 'z'])
        ]
        ordering = ['ore_class', 'count']


class ClusterLayout(Model):
    """
    Contains layout date of clusters since each cluster can be laid out many
    times.
    """
    cluster = ForeignKey(Cluster, on_delete=PROTECT)
    layout_date = DateField(
        help_text='''Date when the cluster is laid out on the field. This date
        cannot be filled out when the date scheduled is still empty.'''
    )


class Crest(Model):
    """
    Polygon version of a crest from Slice.
    """
    slice = OneToOneField('Slice', null=True, blank=True, on_delete=SET_NULL)
    z = PositiveSmallIntegerField()
    geom = MultiPolygonField(srid=3125)

    class Meta:
        indexes = [Index(fields=['z'])]


class DrillHole(Model):
    """
    Drill hole collar technical descriptions.
    """
    name = NameField(max_length=20, unique=True)
    date_drilled = DateField(null=True, blank=True)
    local_block = CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text='block location in local coordinates'
    )
    local_easting = CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text='collar x-coordinates in local grid'
    )
    local_northing = CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text='collar y-coordinates in local grid'
    )
    local_z = FloatField(
        null=True,
        blank=True,
        help_text='collar elevation prior to the use of SRID:3125'
    )
    x = FloatField(
        null=True, blank=True, help_text='collar x-coordinates in SRID:3125'
    )
    y = FloatField(
        null=True, blank=True, help_text='collar y-coordinates in SRID:3125'
    )
    z = FloatField(null=True, blank=True, help_text='collar elevation')
    z_present = FloatField(
        null=True, blank=True, help_text='present ground elevation'
    )
    geom = PointField(srid=3125, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class MineBlock(Model):
    name = MineBlockField(max_length=20, unique=True)
    ridge = CharField(max_length=2, choices=RIDGES)
    geom = PolygonField(srid=3125, null=True, blank=True)

    class Meta:
        ordering = ['ridge', 'name']

    def __str__(self):
        return f'{self.ridge} MB {self.name}'


class Slice(Model):
    """
    A line string representing an element of a mine plan.
    """
    z = IntegerField(help_text="Target elevation of the slice.")
    layer = IntegerField(help_text="""String id.
        2: Crest Line (closed line string)
        7: Road
        8: Toe Line""")
    geom = LineStringField(srid=3125, dim=3)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(layer__in=[2, 7, 8]),
                name='valid_layer'
            ),
        ]
        indexes = [Index(fields=['z'])]


class Stockpile(Model):
    """
    An area wherein mined materials are temporarily placed. Each area can be
    composed of multiple piles.
    """
    name = NameField(max_length=100, unique=True)
    geom = MultiPolygonField(srid=3125, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'
