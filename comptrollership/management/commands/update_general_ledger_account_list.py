from django.core.management.base import BaseCommand
from pathlib import Path

from comptrollership.functions import import_gl_accounts


class Command(BaseCommand):
    help = 'Updates the general ledget account list using a csv file with equivalent headers'

    def add_arguments(self, parser):
        parser.add_argument('source_file', nargs=1, type=Path)
        parser.add_argument('--disable-log', action='store_false')

    def handle(self, *args, **options):
        return import_gl_accounts(options['source_file'][0], options['disable_log'])
