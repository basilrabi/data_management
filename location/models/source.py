from django.contrib.gis.db import models

from custom.fields import MineBlockField, PileField

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
    A group of adjacent `inventory.Blocks` with the same elevation.
    """
    name = models.CharField(max_length=30)
    z = models.SmallIntegerField(default=0)
    ore_class = models.CharField(max_length=1, null=True, blank=True)
    mine_block = models.CharField(max_length=20, null=True, blank=True)
    ni = models.FloatField(default=0)
    fe = models.FloatField(default=0)
    co = models.FloatField(default=0)
    with_layout = models.BooleanField(default=False)
    excavated = models.BooleanField(default=False)
    geom = models.MultiPolygonField(srid=3125, null=True, blank=True)

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
