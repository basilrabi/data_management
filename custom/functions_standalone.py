"""
These are functions that do not import from class-containing modules to prevent
circular import.
"""

from datetime import datetime
from django.utils.dateformat import MONTHS

from .variables import tz_manila

def month_choices() -> list[(str, str)]:
    return [(str(month_num), month_name) for month_num, month_name in MONTHS.items()]

def print_tz_manila(timestamp: datetime) -> (str | None):
    """
    Print the datetime object to a Philippine time stamp without the time zone
    information.
    """
    if timestamp:
        timestamp = str(timestamp.astimezone(tz_manila))
        return timestamp[:-6]
