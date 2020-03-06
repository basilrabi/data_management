import csv
import sys

from django.utils.dateparse import parse_date as pd

from location.models.source import DrillHole
from sampling.models.sample import DrillCoreSample, Lithology

# pylint: disable=no-member

with open('data/sampling_drillcoresample.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['date_received_for_preparation',
                                                 'date_prepared',
                                                 'date_received_for_analysis',
                                                 'date_analyzed',
                                                 'al',
                                                 'c',
                                                 'co',
                                                 'cr',
                                                 'fe',
                                                 'mg',
                                                 'ni',
                                                 'sc',
                                                 'si',
                                                 'moisture',
                                                 'drillhole',
                                                 'interval_from',
                                                 'interval_to',
                                                 'lithology',
                                                 'description',
                                                 'excavated_date'])
    for row in reader:
        #print(f"Drillhole: {row['drillhole']}")
        drillhole = DrillHole.objects.get(name=row['drillhole'])
        if row['lithology'] != '' :
            lithology = Lithology.objects.get(name=row['lithology'])
        else:
            lithology = None
        core = DrillCoreSample(date_received_for_preparation=pd(row['date_received_for_preparation']),
                               date_prepared=pd(row['date_prepared']),
                               date_received_for_analysis=pd(row['date_received_for_analysis']),
                               date_analyzed=pd(row['date_analyzed']),
                               al=row['al'] or None,
                               c=row['c'] or None,
                               co=row['co'] or None,
                               cr=row['cr'] or None,
                               fe=row['fe'] or None,
                               mg=row['mg'] or None,
                               ni=row['ni'] or None,
                               sc=row['sc'] or None,
                               si=row['si'] or None,
                               moisture=row['moisture'] or None,
                               drill_hole=drillhole,
                               interval_from=float(row['interval_from']),
                               interval_to=float(row['interval_to']),
                               lithology=lithology,
                               description=row['description'],
                               excavated_date=pd(row['excavated_date']))
        try:
            #core.clean()
            core.save()
            print(f'Core sample {core.drill_hole.name} {core.interval_from}:{core.interval_to} saved.')
        except KeyboardInterrupt:
            print('\nUploading interrupted.')
            sys.exit(1)
        except Exception as e:
            print(f'Core sample {core.drill_hole.name} {core.interval_from}:{core.interval_to} not saved.')
            print(e)
            sys.exit(1)
        sys.stdout.flush()
        sys.stderr.flush()
