from custom.models import Classification
from django.db.models import  BooleanField, CharField, ForeignKey, Model, PROTECT


class Organization(Classification):

    service_choice = (
        ('Contractor', 'Contractor'),
        ('Operating Company', 'OpCo'),
        ('Government Agency', 'Govt')
    )

    service = CharField(max_length = 30, choices=service_choice, null=True, blank= False)
    active = BooleanField(default=True)


class Department(Model):
    name = CharField(max_length=30, null=True, blank=False)
    abbreviation = CharField(max_length=10, null=True, blank=False)
    parent_division = ForeignKey('Division', on_delete=PROTECT)


class Division(Model):
    name = CharField(max_length=30, null=True, blank=False)
    abbreviation = CharField(max_length=10, null=True, blank=False)

    def __str___(self):
        return self.Name


class Section(Model):
    name = CharField(max_length=30, null=True, blank=False)
    parent_division = ForeignKey('Department', on_delete=PROTECT)