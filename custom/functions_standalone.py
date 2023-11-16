"""
These are functions that do not import from class-containing modules to prevent
circular import.
"""

from datetime import datetime
from django.utils.dateformat import MONTHS
from re import sub

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

def render_to_string(template: str, context: dict[str, str]) -> (str | None):
    """
    An implementation of django.template.loader.render_to_string using raw
    strings to avoid referring to a template.
    """
    if template:
        rendered = template
        for key, value in context.items():
            rendered = sub(rf"{{{{\s*{key}\s*}}}}", value, rendered)
        return rendered
    return None

