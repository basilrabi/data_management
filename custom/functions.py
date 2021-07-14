import csv

from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from django.db import connection
from django.db.models import CheckConstraint, Q
from django.db.models.expressions import Value
from django.db.models.functions import TruncDay
from django.db.models.functions.mixins import FixDecimalInputMixin
from django.db.models.lookups import Transform
from django.http import FileResponse, StreamingHttpResponse
from django.utils.dateparse import parse_datetime as pdt
from os.path import join
from subprocess import PIPE, run
from tempfile import TemporaryDirectory
from tzlocal import get_localzone

from location.models.source import Cluster
from .variables import (
    one_day,
    one_hour,
    one_minute,
    one_second,
    tz_manila,
    zero_time
)


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


# TODO: Delete in Django 3.3
class Round(FixDecimalInputMixin, Transform):
    function = 'ROUND'
    lookup_name = 'round'
    arity = None

    def __init__(self, expression, precision=0, **extra):
        super().__init__(expression, precision, **extra)

    def as_sqlite(self, compiler, connection, **extra_context):
        precision = self.get_source_expressions()[1]
        if isinstance(precision, Value) and precision.value < 0:
            raise ValueError('SQLite does not support negative precision.')
        return super().as_sqlite(compiler, connection, **extra_context)

    def _resolve_output_field(self):
        source = self.get_source_expressions()[0]
        return source.output_field


def export_csv(rows, filename):
    buffer = Echo()
    writer = csv.writer(buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; ' + f'filename="{filename}.csv"'
    return response

def export_sql(sql, csvfile, header=True):
    if header:
        head='HEADER'
    else:
        head=''
    with open(f'scripts/sql/select/{sql}.pgsql', 'r') as file:
        query = file.read().replace('\n', ' ')
        with TemporaryDirectory() as tempdir:
            command = f'cd "{tempdir}" && ' + \
                f'cmd="\\COPY ({query}) TO \'{csvfile}.csv\' ' + \
                f'WITH CSV {head}" && ' + \
                f'psql ' + \
                f'-h {settings.DB_HOST} ' + \
                f'-U  {settings.DB_USER} ' + \
                f'{settings.DB_NAME} ' + \
                f'-c "$cmd"'
            filename = join(tempdir, f'{csvfile}.csv')
            run(command, shell=True, stdout=PIPE, stderr=PIPE)
            return FileResponse(open(filename, 'rb'), content_type='text/csv')

def get_assay_constraints(data):
    return [
        CheckConstraint(check=Q(al__lte=100), name=f'al_max_100_{data}'),
        CheckConstraint(check=Q(al2o3__lte=100), name=f'al2o3_max_100_{data}'),
        CheckConstraint(check=Q(arsenic__lte=100), name=f'arsenic_max_100_{data}'),
        CheckConstraint(check=Q(c__lte=100), name=f'c_max_100_{data}'),
        CheckConstraint(check=Q(cao__lte=100), name=f'cao_max_100_{data}'),
        CheckConstraint(check=Q(co__lte=100), name=f'co_max_100_{data}'),
        CheckConstraint(check=Q(cr__lte=100), name=f'cr_max_100_{data}'),
        CheckConstraint(check=Q(fe__lte=100), name=f'fe_max_100_{data}'),
        CheckConstraint(check=Q(mg__lte=100), name=f'mg_max_100_{data}'),
        CheckConstraint(check=Q(mgo__lte=100), name=f'mgo_max_100_{data}'),
        CheckConstraint(check=Q(mn__lte=100), name=f'mn_max_100_{data}'),
        CheckConstraint(check=Q(ni__lte=100), name=f'ni_max_100_{data}'),
        CheckConstraint(check=Q(p__lte=100), name=f'p_max_100_{data}'),
        CheckConstraint(check=Q(s__lte=100), name=f's_max_100_{data}'),
        CheckConstraint(check=Q(sc__lte=100), name=f'sc_max_100_{data}'),
        CheckConstraint(check=Q(si__lte=100), name=f'si_max_100_{data}'),
        CheckConstraint(check=Q(sio2__lte=100), name=f'sio2_max_100_{data}'),
        CheckConstraint(check=Q(ignition_loss__lte=100), name=f'ignition_loss_max_100_{data}'),
        CheckConstraint(check=Q(moisture__lte=100), name=f'moisture_max_100_{data}'),
        CheckConstraint(check=Q(al__gte=0), name=f'al_min_0_{data}'),
        CheckConstraint(check=Q(al2o3__gte=0), name=f'al2o3_min_0_{data}'),
        CheckConstraint(check=Q(arsenic__gte=0), name=f'arsenic_min_0_{data}'),
        CheckConstraint(check=Q(c__gte=0), name=f'c_min_0_{data}'),
        CheckConstraint(check=Q(cao__gte=0), name=f'cao_min_0_{data}'),
        CheckConstraint(check=Q(co__gte=0), name=f'co_min_0_{data}'),
        CheckConstraint(check=Q(cr__gte=0), name=f'cr_min_0_{data}'),
        CheckConstraint(check=Q(fe__gte=0), name=f'fe_min_0_{data}'),
        CheckConstraint(check=Q(mg__gte=0), name=f'mg_min_0_{data}'),
        CheckConstraint(check=Q(mgo__gte=0), name=f'mgo_min_0_{data}'),
        CheckConstraint(check=Q(mn__gte=0), name=f'mn_min_0_{data}'),
        CheckConstraint(check=Q(ni__gte=0), name=f'ni_min_0_{data}'),
        CheckConstraint(check=Q(p__gte=0), name=f'p_min_0_{data}'),
        CheckConstraint(check=Q(s__gte=0), name=f's_min_0_{data}'),
        CheckConstraint(check=Q(sc__gte=0), name=f'sc_min_0_{data}'),
        CheckConstraint(check=Q(si__gte=0), name=f'si_min_0_{data}'),
        CheckConstraint(check=Q(sio2__gte=0), name=f'sio2_min_0_{data}'),
        CheckConstraint(check=Q(ignition_loss__gte=0), name=f'ignition_loss_min_0_{data}'),
        CheckConstraint(check=Q(moisture__gte=0), name=f'moisture_min_0_{data}')
    ]

def get_optimum_print_slice(queryset, slice_limit=36, lines_allowed=36, space_weight=0.42):
    if get_printed_lines(queryset, queryset.count(), space_weight) <= lines_allowed:
        return queryset.count()
    elif get_printed_lines(queryset, slice_limit, space_weight) <= lines_allowed:
        return slice_limit
    else:
        return get_optimum_print_slice(queryset, slice_limit - 1, lines_allowed, space_weight)

def get_printed_lines(queryset, slice_limit, space_weight):
    """
    Time interval list is printed in PDF for the lay time statement. Each day
    entry is separated by a vertical space. This outputs the estimated number
    of lines given a list of time interval.
    """
    qs = queryset[:slice_limit]
    days = len(set(
        qs.annotate(days=TruncDay('interval_from')).values_list('days')
    ))
    remark_lines = 0
    for detail in qs:
        remark_lines += detail.printed_lines()
    return remark_lines + (days * space_weight) - 1

def mine_blocks_with_clusters():
    # pylint: disable=no-member
    clustered_mine_blocks = set(
        Cluster.objects.values_list('mine_block', flat=True).distinct()
    )
    mine_blocks = list(filter(None, clustered_mine_blocks))
    mine_blocks.sort()
    return mine_blocks

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

def refresh_loading_rate():
    with connection.cursor() as cursor:
            cursor.execute('REFRESH MATERIALIZED VIEW CONCURRENTLY shipment_loadingrate')

def refresh_shipment_number():
    with connection.cursor() as cursor:
            cursor.execute('REFRESH MATERIALIZED VIEW CONCURRENTLY shipment_number')

def round_second(duration):
    seconds = duration.total_seconds()
    return timedelta(seconds=round(seconds, 0))

def round_up_day(timestamp):
    timestamp += one_day
    timestamp = str(print_localzone(timestamp))
    return pdt(f'{timestamp[0:10]} 00:00:00+{timestamp[-5:]}')

def run_sql(pgsql):
    with open(f'scripts/sql/{pgsql}.pgsql', 'r') as file:
        query = file.read()
        with connection.cursor() as cursor:
            cursor.execute(query)

def setup_triggers():
    pgsql = [
        'constraint/location_slice',
        'dump/location_mineblock',
        'function/get_ore_class',
        'function/insert_dummy_cluster',
        'function/shipment_name_html',
        'lock/location_cluster',
        'lock/location_clusterlayout',
        'lock/location_slice',
        'select/shipment_loadingrate',
        'select/shipment_number',
        'index/shipment_loadingrate',
        'index/shipment_number',
        'trigger/inventory_block_exposed',
        'trigger/location_anchorage_update',
        'trigger/location_clippedcluster_insert',
        'trigger/location_clippedcluster_update',
        'trigger/location_cluster_insert',
        'trigger/location_cluster_update',
        'trigger/location_clusterlayout',
        'trigger/location_crest_insert',
        'trigger/location_crest_update',
        'trigger/location_drillhole_update'
    ]
    for query in pgsql:
        run_sql(query)

def this_year():
    return datetime.today().year

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

def to_latex(text):
    """
    Escapes characters to for latex printing.
    """
    return text.replace('&', '\\&')
