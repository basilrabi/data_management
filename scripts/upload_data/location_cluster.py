import csv
import sys
from django.contrib.gis.geos import GEOSGeometry
from inventory.models.insitu import Block
from location.models.source import Cluster
# pylint: disable=no-member
with open('data/location_cluster.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['name',
                                                 'z',
                                                 'ore_class',
                                                 'mine_block',
                                                 'ni',
                                                 'fe',
                                                 'co',
                                                 'with_layout',
                                                 'excavated',
                                                 'geom'])
    for row in reader:
        cluster = Cluster(name=row['name'],
                          z=row['z'],
                          ore_class=row['ore_class'],
                          mine_block=row['mine_block'],
                          ni=row['ni'],
                          fe=row['fe'],
                          co=row['co'],
                          with_layout=row['with_layout'],
                          excavated=row['excavated'],
                          geom=GEOSGeometry(row['geom']))
        try:
            cluster.save()
            print(f'Cluster {cluster.id} saved.')
        except KeyboardInterrupt:
            print('\nUploading interrupted.')
            break
        except:
            print(f'Cluster {cluster.name}-{cluster.z} was not saved.')
        sys.stdout.flush()
        sys.stderr.flush()

with open('data/inventory_clustered_block.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['name'])
    for row in reader:
        block = Block.objects.get(name=row['name'])
        try:
            cluster = Cluster.objects.get(z=block.z,
                                          geom__intersects=block.geom)
            block.cluster = cluster
            block.save()
            print(f'Clustered Block {block.name} saved.')
        except KeyboardInterrupt:
            print('\nUploading interrupted.')
            break
        except:
            print(f'Cluster Block {block.name} was not saved.')
        sys.stdout.flush()
        sys.stderr.flush()
