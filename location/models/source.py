from django.contrib.gis.db import models

from custom.fields import MineBlockField, PileField

RIDGES = (
    ('HY', 'Hayanggabon'),
    ('T1', 'Taga 1'),
    ('T2', 'Taga 2'),
    ('T3', 'Taga 3'),
    ('UZ', 'Urbiztondo'),
    ('KB', 'Kinalablaban')
)

class MineBlock(models.Model):
    name = MineBlockField(max_length=20, unique=True)
    ridge = models.CharField(max_length=2, choices=RIDGES)
    geom = models.PolygonField(srid=3125, null=True, blank=True)

    class Meta:
        ordering = ['ridge', 'name']

    def __str__(self):
        return '{} MB {}'.format(self.ridge, self.name)

class Stockyard(models.Model):
    name = PileField(max_length=20, unique=True)
    geom = models.MultiPolygonField(srid=3125, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '{}'.format(self.name)
