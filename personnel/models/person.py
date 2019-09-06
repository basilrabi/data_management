from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django.db import models

from custom.fields import NameField

class Designation(models.Model):
    name = NameField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class EmploymentRecord(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    effectivity = models.DateField()
    end = models.DateField(null=True, blank=True)
    designation = models.ForeignKey(
        'Designation', on_delete=models.SET_NULL, null=True, blank=True
    )

    def clean(self):
        if not self.effectivity:
            raise ValidationError('Must enter date of effectivity.')
        if self.end:
            if self.end <= self.effectivity:
                raise ValidationError('Effectivity must be earlier than end.')
        # pylint: disable=E1101
        if self.person.employmentrecord_set.filter(
            models.Q(
                effectivity__lte=self.end or self.effectivity + timedelta(9999)
            ),
            models.Q(end__gte=self.effectivity) |
            models.Q(end__isnull=True)
        ).exclude(id=self.id).count() > 0:
            raise ValidationError('Effectivity should not overlap.')

    class Meta:
        ordering = ['-effectivity']

    def __str__(self):
        return '{} as {}'.format(self.person.__str__(),
                                 self.designation.__str__())

class Person(models.Model):
    first_name = NameField(max_length=100)
    middle_name = NameField(max_length=100, null=True, blank=True)
    last_name = NameField(max_length=100)
    name_suffix = NameField(
        max_length=20, null=True, blank=True,
        help_text='Junior, Senior, III, etc.'
    )

    def designation(self, date):
        # pylint: disable=E1101
        if self.employmentrecord_set.all().count() > 0:
            return self.employmentrecord_set.filter(
                models.Q(effectivity__lte=date),
                models.Q(end__gte=date) |
                models.Q(end__isnull=True)
            ).first().designation

    def present_designation(self):
        return self.designation(date.today())

    class Meta:
        ordering = ['last_name', 'first_name', 'middle_name']

    def __str__(self):
        if self.name_suffix:
            return '{}, {} {}' \
                .format(self.last_name, self.first_name, self.name_suffix)
        else:
            return '{}, {}'.format(self.last_name, self.first_name)
