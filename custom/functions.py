import csv
import re

from datetime import datetime, timedelta
from django.db.transaction import on_commit
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.db import connection
from django.db.models import CheckConstraint, Q
from django.db.models.expressions import Value
from django.db.models.functions import TruncDay
from django.db.models.functions.mixins import FixDecimalInputMixin
from django.db.models.lookups import Transform
from django.db.models.query import QuerySet
from django.http import FileResponse, StreamingHttpResponse
from django.utils.dateparse import parse_datetime as pdt
from os.path import join
from subprocess import PIPE, run
from tempfile import TemporaryDirectory
from typing import Iterable
from tzlocal import get_localzone

from fleet.models.equipment import Equipment, EquipmentClass
from gammu import EncodeSMS
from gammu.smsd import SMSD
from os import environ
from organization.models import Organization
from location.models.equipment import EquipmentLocation
from location.models.landuse import MPSA
from location.models.source import Cluster
from .models import Log, MobileNumber, User
from .variables import (
    one_day,
    one_hour,
    one_minute,
    one_second,
    zero_time
)

smsd = SMSD(f'{environ["HOME"]}/gammu-smsdrc')


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


def export_csv(rows: Iterable[list[str]], filename: str) -> StreamingHttpResponse:
    """
    Export a csv stream from python generated rows.
    """
    buffer = Echo()
    writer = csv.writer(buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows), content_type="text/csv")
    response['Content-Disposition'] = 'attachment; ' + f'filename="{filename}.csv"'
    return response

def export_sql(sql: str, csvfile: str, header: bool = True) -> FileResponse:
    """
    Export a csv file from a PostgreSQL query file.
    """
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

def get_assay_constraints(data: str) -> list[CheckConstraint]:
    """
    Returns a list of constraints for all Assay-like objects.
    """
    return [
        CheckConstraint(check=Q(al__lte=100), name=f'al_max_100_{data}'),
        CheckConstraint(check=Q(al2o3__lte=100), name=f'al2o3_max_100_{data}'),
        CheckConstraint(check=Q(arsenic__lte=100), name=f'arsenic_max_100_{data}'),
        CheckConstraint(check=Q(c__lte=100), name=f'c_max_100_{data}'),
        CheckConstraint(check=Q(cao__lte=100), name=f'cao_max_100_{data}'),
        CheckConstraint(check=Q(co__lte=100), name=f'co_max_100_{data}'),
        CheckConstraint(check=Q(cr__lte=100), name=f'cr_max_100_{data}'),
        CheckConstraint(check=Q(cr2o3__lte=100), name=f'cr2o3_max_100_{data}'),
        CheckConstraint(check=Q(cu__lte=100), name=f'cu_max_100_{data}'),
        CheckConstraint(check=Q(fe__lte=100), name=f'fe_max_100_{data}'),
        CheckConstraint(check=Q(k__lte=100), name=f'k_max_100_{data}'),
        CheckConstraint(check=Q(mg__lte=100), name=f'mg_max_100_{data}'),
        CheckConstraint(check=Q(mgo__lte=100), name=f'mgo_max_100_{data}'),
        CheckConstraint(check=Q(mn__lte=100), name=f'mn_max_100_{data}'),
        CheckConstraint(check=Q(ni__lte=100), name=f'ni_max_100_{data}'),
        CheckConstraint(check=Q(p__lte=100), name=f'p_max_100_{data}'),
        CheckConstraint(check=Q(pb__lte=100), name=f'pb_max_100_{data}'),
        CheckConstraint(check=Q(s__lte=100), name=f's_max_100_{data}'),
        CheckConstraint(check=Q(sc__lte=100), name=f'sc_max_100_{data}'),
        CheckConstraint(check=Q(si__lte=100), name=f'si_max_100_{data}'),
        CheckConstraint(check=Q(sio2__lte=100), name=f'sio2_max_100_{data}'),
        CheckConstraint(check=Q(zn__lte=100), name=f'zn_max_100_{data}'),
        CheckConstraint(check=Q(ignition_loss__lte=100), name=f'ignition_loss_max_100_{data}'),
        CheckConstraint(check=Q(moisture__lte=100), name=f'moisture_max_100_{data}'),
        CheckConstraint(check=Q(al__gte=0), name=f'al_min_0_{data}'),
        CheckConstraint(check=Q(al2o3__gte=0), name=f'al2o3_min_0_{data}'),
        CheckConstraint(check=Q(arsenic__gte=0), name=f'arsenic_min_0_{data}'),
        CheckConstraint(check=Q(c__gte=0), name=f'c_min_0_{data}'),
        CheckConstraint(check=Q(cao__gte=0), name=f'cao_min_0_{data}'),
        CheckConstraint(check=Q(co__gte=0), name=f'co_min_0_{data}'),
        CheckConstraint(check=Q(cr__gte=0), name=f'cr_min_0_{data}'),
        CheckConstraint(check=Q(cr2o3__gte=0), name=f'cr2o3_min_0_{data}'),
        CheckConstraint(check=Q(cu__gte=0), name=f'cu_min_0_{data}'),
        CheckConstraint(check=Q(fe__gte=0), name=f'fe_min_0_{data}'),
        CheckConstraint(check=Q(k__gte=0), name=f'k_min_0_{data}'),
        CheckConstraint(check=Q(mg__gte=0), name=f'mg_min_0_{data}'),
        CheckConstraint(check=Q(mgo__gte=0), name=f'mgo_min_0_{data}'),
        CheckConstraint(check=Q(mn__gte=0), name=f'mn_min_0_{data}'),
        CheckConstraint(check=Q(ni__gte=0), name=f'ni_min_0_{data}'),
        CheckConstraint(check=Q(p__gte=0), name=f'p_min_0_{data}'),
        CheckConstraint(check=Q(pb__gte=0), name=f'pb_min_0_{data}'),
        CheckConstraint(check=Q(s__gte=0), name=f's_min_0_{data}'),
        CheckConstraint(check=Q(sc__gte=0), name=f'sc_min_0_{data}'),
        CheckConstraint(check=Q(si__gte=0), name=f'si_min_0_{data}'),
        CheckConstraint(check=Q(sio2__gte=0), name=f'sio2_min_0_{data}'),
        CheckConstraint(check=Q(zn__gte=0), name=f'zn_min_0_{data}'),
        CheckConstraint(check=Q(ignition_loss__gte=0), name=f'ignition_loss_min_0_{data}'),
        CheckConstraint(check=Q(moisture__gte=0), name=f'moisture_min_0_{data}')
    ]

def get_optimum_print_slice(queryset: QuerySet, slice_limit=36, lines_allowed=36, space_weight=0.42) -> int:
    """
    Estimate the optimum number of interval objects to be printed in the first
    page ofthe laydays statement.
    """
    if get_printed_lines(queryset, queryset.count(), space_weight) <= lines_allowed:
        return queryset.count()
    elif get_printed_lines(queryset, slice_limit, space_weight) <= lines_allowed:
        return slice_limit
    else:
        return get_optimum_print_slice(queryset, slice_limit - 1, lines_allowed, space_weight)

def get_printed_lines(queryset: QuerySet, slice_limit: int, space_weight: float) -> float:
    """
    Time interval list is printed in PDF for the lay time statement. Each day
    entry is separated by a vertical space. This outputs the estimated number
    of printed lines in the PDF given a list of time interval.
    """
    qs = queryset[:slice_limit]
    days = len(set(
        qs.annotate(days=TruncDay('interval_from')).values_list('days')
    ))
    remark_lines = 0
    for detail in qs:
        remark_lines += detail.printed_lines()
    return remark_lines + (days * space_weight) - 1

def get_sender(number: str) -> (User | None):
    """
    Return the owner of the mobile number.
    """
    sender = MobileNumber.objects.filter(spaceless_number=number)
    if sender.exists():
        return sender.first().user

def mine_blocks_with_clusters() -> list[str]:
    """
    Return the mine blocks containing a cluster. This is used for filtering in
    the admin page.
    """
    clustered_mine_blocks = set(
        Cluster.objects.values_list('mine_block', flat=True).distinct()
    )
    mine_blocks = list(filter(None, clustered_mine_blocks))
    mine_blocks.sort()
    return mine_blocks

def on_transaction_commmit(func):
    def inner(*args, **kwargs):
        on_commit(lambda: func(*args, **kwargs))
    return inner

def ordinal_suffix(x: str) -> str:
    """
    Append the proper ordinal suffix given a whole number.
    """
    x = int(x)
    if x % 100 in (11, 12, 13):
        return 'th'
    x %= 10
    suffix = ['st', 'nd', 'rd']
    if x in (0, 4, 5, 6, 7, 8, 9):
        return 'th'
    return suffix[x-1]

def print_localzone(timestamp: datetime) -> (datetime | None):
    """
    Convert a datetime object to the timezone in the localmachine.
    """
    if timestamp:
        return timestamp.astimezone(get_localzone())

def refresh_loading_rate() -> None:
    """
    Refresh the view shipment_loadingrate.
    """
    with connection.cursor() as cursor:
        cursor.execute('REFRESH MATERIALIZED VIEW CONCURRENTLY shipment_loadingrate')

def refresh_shipment_number() -> None:
    """
    Refresh the view shipment_number.
    """
    with connection.cursor() as cursor:
        cursor.execute('REFRESH MATERIALIZED VIEW CONCURRENTLY shipment_number')

def round_second(duration: timedelta) -> timedelta:
    """
    Round a duration to the nearest second since human readers of the printed
    laydays statement can only digest this level of accuracy. Any smaller than
    this is impractical.
    """
    seconds = duration.total_seconds()
    return timedelta(seconds=round(seconds, 0))

def round_up_day(timestamp: datetime) -> datetime:
    """
    Rounds up a datetime object to the nearest day in the local time zone.
    """
    timestamp += one_day
    timestamp = str(print_localzone(timestamp))
    return pdt(f'{timestamp[0:10]} 00:00:00+{timestamp[-5:]}')

def run_sql(pgsql: str) -> None:
    """
    Execute a file containing a PostgreSQL query.
    """
    with open(f'scripts/sql/{pgsql}.pgsql', 'r') as file:
        query = file.read()
        with connection.cursor() as cursor:
            cursor.execute(query)

def send_sms(number: str, text: str) -> None:
    """
    Injects a text to Gammu SMSD.
    """
    Log(log=f'Sending SMS to {number}:\n{text}').save()
    if len(text) <= 160:
        log = smsd.InjectSMS([{
            'Number': f'{number}',
            'SMSC': {'Location': 1},
            'Text': f'{text}'
        }])
        Log(log=f'Injected SMS: {log}').save()
    else:
        smsinfo = {
            'Class': -1,
            'Entries': [{'ID': 'ConcatenatedTextLong', 'Buffer': f'{text}'}]
        }
        for message in EncodeSMS(smsinfo):
            message["SMSC"] = {'Location': 1}
            message["Number"] = f'{number}'
            log = smsd.InjectSMS([message])
            Log(log=f'Injected SMS: {log}').save()

def setup_triggers() -> None:
    """
    Initializes all needed database objects for testing.
    """
    pgsql = [
        'constraint/location_slice',
        'dump/location_mineblock',
        'dump/location_mpsa',
        'function/array_from_geom',
        'function/get_ore_class',
        'function/gradient',
        'function/shipment_name_html',
        'function/slope_angle',
        'function/vectors',
        'procedure/insert_dummy_cluster',
        'procedure/record_log',
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
        'trigger/location_drillhole_update',
        'trigger/organization_organizationunit_delete',
        'trigger/organization_organizationunit_insert',
        'trigger/organization_organizationunit_update',
        'trigger/shipment_trip_update'
    ]
    for query in pgsql:
        run_sql(query)

def sms_response(sms: str, sender: User) -> str:
    """
    Drafts an SMS response to any SMS received by the server. When a valid
    equipment location pattern is received, saves an EquipmentLocation object
    using the information received.
    """
    message = re.sub('\s+', ' ', sms).strip().upper()
    if message == 'FORTUNE' or message == '':
        return run('fortune', stdout=PIPE).stdout.decode('utf-8') \
            .replace('\t', '    ') \
            .replace('`', "'").rstrip()

    location_pattern_general_decimal = re.compile('^(\w+)\s(\w+)\s(\d+)\s(\d+(\.\d+)?)\s(\d+(\.\d+)?)$')
    location_pattern_general_dms = re.compile('^(\w+)\s(\w+)\s(\d+)\s(\d+)\s(\d+)\s(\d+(\.\d+)?)\s(\d+)\s(\d+)\s(\d+(\.\d+)?)$')
    location_pattern_inhouse_decimal = re.compile('^(\w+)\s(\d+)\s(\d+(\.\d+)?)\s(\d+(\.\d+)?)$')
    location_pattern_inhouse_dms = re.compile('^(\w+)\s(\d+)\s(\d+)\s(\d+)\s(\d+(\.\d+)?)\s(\d+)\s(\d+)\s(\d+(\.\d+)?)$')

    if location_pattern_inhouse_decimal.match(message) or location_pattern_inhouse_dms.match(message):
        match_dec = False
        if location_pattern_inhouse_decimal.match(message):
            match = location_pattern_inhouse_decimal.match(message)
            match_dec = True
        else:
            match = location_pattern_inhouse_dms.match(message)

        equipment_class = EquipmentClass.objects.filter(name=match.group(1))
        if equipment_class.exists():
            equipment = Equipment.objects.filter(
                fleet_number=int(match.group(2)),
                model__equipment_class__name=match.group(1),
                owner__name='TMC'
            )
            if equipment.exists():
                equipment = equipment.first()
                if match_dec:
                    geom = GEOSGeometry(f'SRID=4326;POINT({match.group(3)} {match.group(5)})')
                else:
                    lat_deg = float(match.group(7))
                    lat_min = float(match.group(8))
                    lat_sec = float(match.group(9))
                    lon_deg = float(match.group(3))
                    lon_min = float(match.group(4))
                    lon_sec = float(match.group(5))
                    lat = lat_deg + (lat_min / 60) + (lat_sec / 3600)
                    lon = lon_deg + (lon_min / 60) + (lon_sec / 3600)
                    geom = GEOSGeometry(f'SRID=4326;POINT({lon:.12} {lat:.10})')
                if MPSA.objects.filter(geom__distance_lt=(geom, D(km=5))).exists():
                    EquipmentLocation(
                        equipment=equipment,
                        user=sender,
                        geom=geom
                    ).save()
                    return f'Location saved for {equipment}. Thank you {sender.first_name or sender.__str__()}.'
                else:
                    return f'Invalid location. Input point is 5 km outside MPSA.'
            else:
                return f'TMC {match.group(1)} {match.group(2)} is not yet registered.'
        else:
            class_list = [f'{fleet.name} - {fleet.description}' for fleet in EquipmentClass.objects.all()]
            class_text = '\n'.join(class_list)
            return f'Equipment type "{match.group(1)}" does not exist. Possible choices are:\n{class_text}\n.'

    if location_pattern_general_decimal.match(message) or location_pattern_general_dms.match(message):
        match_dec = False
        if location_pattern_general_decimal.match(message):
            match = location_pattern_general_decimal.match(message)
            match_dec = True
        else:
            match = location_pattern_general_dms.match(message)

        equipment = Equipment.objects.filter(
            fleet_number=int(match.group(3)),
            model__equipment_class__name=match.group(2),
            owner__name=match.group(1)
        )
        if equipment.exists():
            equipment = equipment.first()
            if match_dec:
                geom = GEOSGeometry(f'SRID=4326;POINT({match.group(4)} {match.group(6)})')
            else:
                lat_deg = float(match.group(8))
                lat_min = float(match.group(9))
                lat_sec = float(match.group(10))
                lon_deg = float(match.group(4))
                lon_min = float(match.group(5))
                lon_sec = float(match.group(6))
                lat = lat_deg + (lat_min / 60) + (lat_sec / 3600)
                lon = lon_deg + (lon_min / 60) + (lon_sec / 3600)
                geom = GEOSGeometry(f'SRID=4326;POINT({lon:.12} {lat:.10})')
            if MPSA.objects.filter(geom__distance_lt=(geom, D(km=5))).exists():
                EquipmentLocation(
                    equipment=equipment,
                    user=sender,
                    geom=geom
                ).save()
                return f'Location saved for {equipment}. Thank you {sender.first_name or sender.__str__()}.'
            else:
                return f'Invalid location. Input point is 5 km outside MPSA.'
        else:
            owner = Organization.objects.filter(name=match.group(1))
            if not owner.exists():
                org_list = [f'{org.name} - {org.description}' for org in Organization.objects.all()]
                org_text = '\n'.join(org_list)
                return f'Company "{match.group(1)}" does not exist. Possible choices are:\n{org_text}\n.'
            equipment_class = EquipmentClass.objects.filter(name=match.group(2))
            if not equipment_class.exists():
                class_list = [f'{fleet.name} - {fleet.description}' for fleet in EquipmentClass.objects.all()]
                class_text = '\n'.join(class_list)
                return f'Equipment type "{match.group(2)}" does not exist. Possible choices are:\n{class_text}\n.'
            return f'{match.group(1)} {match.group(2)} {match.group(3)} is not yet registered.'
    else:
        return (
            'Text pattern unrecognized.\n\n'
            'If you want to report the location of an equipment, '
            'you may use the patterns below.\n\n'
            'GENERAL PATTERN (Intended for all equipment units, including contractors):\n\n'
            '[company] [equipment type] [body number] [longitude decimal degree] [latitude decimal degree]\n\n'
            'Example:\n'
            'TMC  DT  234  125.8246  9.5176\n\n'
            '[company] [equipment type] [body number] [longitude degree minute second] [latitude degree minute second]\n\n'
            'Example:\n'
            'TMC  DT  234  125  49  28.56  9  31  3.36\n\n'
            'INHOUSE PATTERN (Intended for TMC equipment only):\n\n'
            '[equipment type] [body number] [longitude decimal degree] [latitude decimal degree]\n'
            'Example:\n'
            'DT  234  125.8246  9.5176\n\n'
            '[equipment type] [body number] [longitude degree minute second] [latitude degree minute second]\n'
            'Example:\n'
            'DT  234  125  49  28.56  9  31  3.36\n\n'
            'The expected coordinate system is WGS 84 (EPSG:4326).'
        )

def to_dhms(duration: timedelta) -> str:
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

def to_hm(duration: timedelta) -> str:
    """
    Converts a datetime.timedelta object to an hm string.
    """
    hours = duration // one_hour
    minutes = (duration - (hours * one_hour)) // one_minute
    return f'{hours:02d}:{minutes:02d}'

def to_hms(duration: timedelta) -> str:
    """
    Converts a datetime.timedelta object to an hms string.
    """
    hours = duration // one_hour
    duration -= hours * one_hour
    minutes = duration // one_minute
    duration -= minutes * one_minute
    seconds = duration // one_second
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'

def to_latex(text: str) -> str:
    """
    Escapes characters to for latex printing.
    """
    return text.replace('&', '\\&')
