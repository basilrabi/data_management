from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db.models import (Model as GeoModel, MultiPolygonField)
from django.db.models import (
    CharField,
    F,
    ForeignKey,
    Model,
    SET_NULL,
    TextField
)
from phonenumber_field.modelfields import PhoneNumberField

from custom.fields import NameField, SpaceLess


class Classification(Model):
    """
    Template for any classification.
    """
    name = NameField(max_length=20, unique=True)
    description = TextField(null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class GeoClassification(GeoModel):
    """
    Template for any classification.
    """
    name = NameField(max_length=40, unique=True)
    description = TextField(null=True, blank=True)
    geom = MultiPolygonField(srid=3125)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class MobileNumber(Model):
    user = ForeignKey('User', null=True, blank=True, on_delete=SET_NULL)
    number = PhoneNumberField(unique=True)
    spaceless_number = SpaceLess(
        null=True, blank=True, unique=True, max_length=20
    )

    def save(self, *args, **kwargs):
        self.spaceless_number = self.number
        super().save(*args, **kwargs)

    class Meta:
        ordering = [F('spaceless_number').asc()]

    def __str__(self):
        return self.spaceless_number


class User(AbstractUser):
    middle_name = CharField(null=True, blank=True, max_length=100)

    def middle_initial(self):
        if self.middle_name:
            mi = [x[:1].upper() for x in str(self.middle_name).split(' ')]
            return '.'.join(mi) + '.'
        return ''
