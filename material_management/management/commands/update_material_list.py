from django.core.management.base import BaseCommand
from pathlib import Path

from material_management.functions import import_material

class Command(BaseCommand):
    help = 'Updates the material list using the input file similar to http://datamanagement.tmc.nickelasia.com:81/static/TMC/material.csv'

    def add_arguments(self, parser):
        parser.add_argument('source_file', nargs=1, type=Path)
        parser.add_argument('--disable-log', action='store_false')

    def handle(self, *args, **options):
        return import_material(options['source_file'][0], options['disable_log'])
