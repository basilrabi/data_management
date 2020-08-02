from django.contrib.auth.models import AbstractUser
from django.db import models

from custom.fields import NameField


class Classification(models.Model):
    """
    Template for any classification.
    """
    name = NameField(max_length=20, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class User(AbstractUser):
    middle_name = models.CharField(null=True, blank=True, max_length=100)

    def middle_initial(self):
        if self.middle_name:
            mi = [x[:1].upper() for x in str(self.middle_name).split(' ')]
            return '.'.join(mi) + '.'
        return ''
