import csv
import datetime

from django.contrib.gis.geos import GEOSGeometry
from django.http import StreamingHttpResponse
from django.utils.dateparse import parse_datetime as pdt
from tzlocal import get_localzone

from .variables import (one_day,
                        one_hour,
                        one_minute,
                        one_second,
                        tz_manila,
                        zero_time)

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

def export_csv(rows, filename):
    buffer = Echo()
    writer = csv.writer(buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; ' + f'filename="{filename}.csv"'
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

def point_to_box(point_geom, distance=5):
    """
    Converts a point geometry to a square with lengh = 2 * distance.
    """
    if point_geom.geom_type != 'Point':
        raise TypeError('Data is not a point geometry.')
    ewkt = f'SRID={point_geom.srid};POLYGON ((' + \
        f'{point_geom.coords[0] - distance} {point_geom.coords[1] - distance}, ' + \
        f'{point_geom.coords[0] - distance} {point_geom.coords[1] + distance}, ' + \
        f'{point_geom.coords[0] + distance} {point_geom.coords[1] + distance}, ' + \
        f'{point_geom.coords[0] + distance} {point_geom.coords[1] - distance}, ' + \
        f'{point_geom.coords[0] - distance} {point_geom.coords[1] - distance}))'
    return GEOSGeometry(ewkt)

def print_localzone(timestamp):
    if timestamp:
        return timestamp.astimezone(get_localzone())

def print_tz_manila(timestamp):
    if timestamp:
        timestamp = str(timestamp.astimezone(tz_manila))
        return timestamp[:-6]

def round_second(duration):
    seconds = duration.total_seconds()
    return datetime.timedelta(seconds=round(seconds, 0))

def round_up_day(timestamp):
    timestamp += one_day
    timestamp = str(print_localzone(timestamp))
    return pdt(f'{timestamp[0:10]} 00:00:00+{timestamp[-5:]}')

def to_dhms(duration):
    """
    Converts a datetime.timedelta object to an dhms string.
    """
    negative = False
    if duration < zero_time:
        negative = True
        duration = -duration
    days = duration // one_day
    duration -= days * one_day
    hours = duration // one_hour
    duration -= hours * one_hour
    minutes = duration // one_minute
    duration -= minutes * one_minute
    seconds = duration // one_second
    dhms = f'{days:02d} {hours:02d}:{minutes:02d}:{seconds:02d}'
    if negative:
        return '-' + dhms
    return dhms

def to_hm(duration):
    """
    Converts a datetime.timedelta object to an hm string.
    """
    hours = duration // one_hour
    minutes = (duration - (hours * one_hour)) // one_minute
    return f'{hours:02d}:{minutes:02d}'

def to_hms(duration):
    """
    Converts a datetime.timedelta object to an hms string.
    """
    hours = duration // one_hour
    duration -= hours * one_hour
    minutes = duration // one_minute
    duration -= minutes * one_minute
    seconds = duration // one_second
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'
