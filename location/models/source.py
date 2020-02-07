from django.contrib.gis.db import models

from custom.fields import MineBlockField, PileField

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
    z = models.IntegerField(default=0)
    mine_block = models.CharField(max_length=20, null=True, blank=True)
    ni = models.FloatField(default=0)
    fe = models.FloatField(default=0)
    co = models.FloatField(default=0)
    with_layout = models.BooleanField(default=False)
    excavated = models.BooleanField(default=False)
    geom = models.MultiPolygonField(srid=3125, null=True, blank=True)

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
