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
