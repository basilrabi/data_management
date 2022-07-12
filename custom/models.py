from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db.models import (Model as GeoModel, MultiPolygonField)
from django.db.models import (
    CharField,
    DateField,
    DateTimeField,
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
    name = NameField(max_length=40, unique=True)
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


class Log(Model):
    """
    Asyncronous log storage
    """
    created = DateTimeField(auto_now_add=True)
    log = TextField()

    class Meta:
        ordering = [F('created').desc()]


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
        return self.number.as_international


class User(AbstractUser):
    middle_name = CharField(null=True, blank=True, max_length=100)
    birth_date = DateField(null=True, blank=True)
    name_suffix = NameField(
        max_length=20,
        null=True,
        blank=True,
        help_text='Junior, Senior, III, etc.'
    )

    SEX_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male'),
        ('N', 'Non-binary')
    )
    sex = CharField(max_length=1, choices=SEX_CHOICES, null=True, blank=True)

    def middle_initial(self):
        if self.middle_name:
            mi = [x[:1].upper() for x in str(self.middle_name).split(' ')]
            return '.'.join(mi) + '.'
        return ''
