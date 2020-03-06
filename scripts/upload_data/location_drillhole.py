import csv
import sys

from django.utils.dateparse import parse_date as pd

from location.models.source import DrillHole

with open('data/location_drillhole.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['name',
                                                 'date_drilled',
                                                 'local_block',
                                                 'local_easting',
                                                 'local_northing',
                                                 'local_z',
                                                 'x',
                                                 'y',
                                                 'z',
                                                 'z_present'])
    for row in reader:
        drillhole = DrillHole(name=row['name'],
                              date_drilled=pd(row['date_drilled']),
                              local_block=row['local_block'],
                              local_easting=row['local_easting'],
                              x=None if row['x'] == '' else float(row['x']),
                              y=None if row['y'] == '' else float(row['y']),
                              z=None if row['z'] == '' else float(row['z']),
                              z_present=None if row['z_present'] == '' else float(row['z_present']))
        try:
            drillhole.save()
            print(f'Drillhole {drillhole.name} saved')
        except KeyboardInterrupt:
            print('\nUploading interrupted.')
            sys.exit(1)
        except Exception as e:
            print(f'Drillhole {drillhole.name} not saved')
            print(e)
            sys.exit(1)
        sys.stdout.flush()
        sys.stderr.flush()
