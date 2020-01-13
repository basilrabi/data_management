import csv
import datetime

from django.db import models
from django.http import StreamingHttpResponse
from re import sub
from tzlocal import get_localzone

from .variables import one_day

class AlphaNumeric(models.CharField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return sub(r'[^\w]', '', str(value).upper())

class Echo:
    """
    An object that implements just the write method of the file-like interface.
    This is copied from the django documentation in creating csv stream view.
    """

    def write(self, value):
        """
        Write the value by returning it, instead of storing in a buffer.
        """
        return value

class MineBlockField(models.CharField):
    """
    This field must always start with a number.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value:
            value = sub(r'^(\D*)*', r'\1', str(value).upper())
            value = sub(r'\W', '', value)
            return value

class NameField(models.CharField):
    """
    https://stackoverflow.com/questions/36330677/
    django-model-set-default-charfield-in-lowercase
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value:
            return sub(r'\s+', ' ', str(value).upper().strip())

class PileField(models.CharField):
    """
    This field must always start with an alphabet
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value:
            value = sub(r'^([^A-Z]*)*', r'\1', str(value).upper())
            value = sub(r'\W', '', value)
            return value

class SpaceLess(models.CharField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value:
            return sub(r'\s+', '', str(value).upper())

class MarineVesselName(models.CharField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value:
            value = sub(r'\s+', ' ', str(value).upper().strip())
            value = sub(r'^M[^a-zA-Z]*V\s*', '', value)
            return value

def export_csv(rows, filename):
    buffer = Echo()
    writer = csv.writer(buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; ' + \
        f'filename="{filename}.csv"'
    return response

def ordinal_suffix(x):
    x = int(x)
    if x % 100 in (11, 12, 13):
        return 'th'
    x %= 10
    suffix = ['st', 'nd', 'rd']
    if x in (0, 4, 5, 6, 7, 8, 9):
        return 'th'
    return suffix[x-1]

def print_localzone(timestamp):
    if timestamp:
        return timestamp.astimezone(get_localzone())

def round_up_day(timestamp):
    return timestamp.combine(
        timestamp.date(), datetime.time(hour=0), timestamp.tzinfo
    ) + one_day
