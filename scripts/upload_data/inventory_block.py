import csv
import sys
from django.contrib.gis.geos import GEOSGeometry
from inventory.models.insitu import Block
# pylint: disable=no-member
with open('data/inventory_block.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['name',
                                                 'z',
                                                 'ni',
                                                 'fe',
                                                 'co',
                                                 'geom'])
    for row in reader:
        block = Block(name=row['name'],
                      z=row['z'],
                      ni=row['ni'],
                      fe=row['fe'],
                      co=row['co'],
                      geom=GEOSGeometry(row['geom']))
        try:
            block.save()
            print(f'Block {block.name} saved.')
        except KeyboardInterrupt:
            print('\nUploading interrupted.')
            break
        except:
            print(f'Block {block.name} was not saved.')
        sys.stdout.flush()
        sys.stderr.flush()
