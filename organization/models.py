from custom.models import Classification
from django.db.models import CharField


class Organization(Classification):
    service_choice = (
        ('Contractor', 'Contractor'),
        ('Operating Company', 'OpCo'),
        ('Government Agency', 'Govt')
    )

    service = CharField(max_length = 30, choices=service_choice, null=True, blank= False)
