from django.db.models import  (
    BooleanField,
    CharField,
    ForeignKey,
    Model, PROTECT
)

from custom.models import Classification


class Department(Model):
    name = CharField(max_length=30, null=True, blank=False, unique=True)
    abbreviation = CharField(max_length=10, null=True, blank=False)
    parent_division = ForeignKey('Division', on_delete=PROTECT)


class Division(Model):
    name = CharField(max_length=30, null=True, blank=False, unique=True)
    abbreviation = CharField(max_length=10, null=True, blank=False)

    def __str__(self):
        return self.name


class Organization(Classification):

    service_choice = (
        ('Contractor', 'Contractor'),
        ('Operating Company', 'OpCo'),
        ('Government Agency', 'Govt')
    )

    service = CharField(max_length = 30, choices=service_choice, null=True, blank= False)
    active = BooleanField(default=True)


class OrganizationUnit(Model):
    """
    Table containing all organization units
    """
    uid = CharField(max_length=15, unique=True)
    name = CharField(max_length=30)
    abbreviation = CharField(max_length=30)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Section(Model):
    name = CharField(max_length=30, null=True, blank=False, unique=True)
    parent_department = ForeignKey('Department', on_delete=PROTECT)
