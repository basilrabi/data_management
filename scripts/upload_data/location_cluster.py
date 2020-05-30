import csv
import sys

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models import Q
from django.utils.dateparse import parse_date as pd

from custom.functions import point_to_box
from inventory.models.insitu import Block
from location.models.landuse import RoadArea
from location.models.source import Cluster

# pylint: disable=no-member

with open('data/location_cluster.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['name',
                                                 'z',
                                                 'distance_from_road',
                                                 'road',
                                                 'date_scheduled',
                                                 'layout_date',
                                                 'geom'])
    for row in reader:
        cluster = Cluster(name=row['name'],
                          z=row['z'],
                          distance_from_road=row['distance_from_road'] or 0,
                          date_scheduled=pd(row['date_scheduled']),
                          layout_date=pd(row['layout_date']),
                          geom=GEOSGeometry(row['geom']))
        if RoadArea.objects.filter(date_surveyed=pd(row['road'])).exists():
            cluster.road = RoadArea.objects.get(date_surveyed=pd(row['road']))
        try:
            cluster.save()
            print(f'Cluster {cluster.id} saved.')
        except KeyboardInterrupt:
            print('\nUploading interrupted.')
            sys.exit(1)
        except Exception as e:
            print(f'Cluster {cluster.name}-{cluster.z} was not saved.')
            print(e)
            sys.exit(1)
        sys.stdout.flush()
        sys.stderr.flush()

with open('data/inventory_clustered_block.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['name'])
    for row in reader:
        block = Block.objects.get(name=row['name'])
        try:
            cluster = Cluster.objects.get(
                Q(z=block.z),
                Q(geom__intersects=block.geom) |
                Q(geom__overlaps=point_to_box(block.geom))
            )
            block.cluster = cluster
            block.save()
            print(f'Clustered Block {block.name} saved.')
        except KeyboardInterrupt:
            print('\nUploading interrupted.')
            sys.exit(1)
        except Exception as e:
            print(f'Clustered Block {block.name} was not saved.')
            print(e)
            sys.exit(1)
        sys.stdout.flush()
        sys.stderr.flush()
