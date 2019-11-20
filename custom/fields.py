from django.db import models
from re import sub

class AlphaNumeric(models.CharField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return sub(r'[^\w]', '', str(value).upper())

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
