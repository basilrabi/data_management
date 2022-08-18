"""
These are functions that do not import from class-containing modules to prevent
circular import.
"""

from datetime import datetime

from .variables import tz_manila

def print_tz_manila(timestamp: datetime) -> (str | None):
    """
    Print the datetime object to a Philippine time stamp without the time zone
    information.
    """
    if timestamp:
        timestamp = str(timestamp.astimezone(tz_manila))
        return timestamp[:-6]
