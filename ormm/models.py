from datetime import datetime
from django.db.models import (
    BooleanField,
    CharField,
    DateField, 
    FileField,
    ForeignKey,
    Max, 
    Model,
    PROTECT,
    TextField
)
from django.utils.html import mark_safe
import re

from .functions import filepath
from organization.models import OrganizationUnit


class ExternalCommunication(Model):

    transmittal_number = CharField(max_length=13, null=False, blank=True, primary_key=True)
    date = DateField(null=True, blank=False)
    requesting_department = ForeignKey(OrganizationUnit, null=True, blank=True, on_delete=PROTECT)
    nature_of_content = TextField(max_length=99, null=True, blank=True)
    recipient = CharField(max_length=30, null=False, blank=False, default='')
    receiving_copy = FileField(upload_to=filepath,null=True, blank=True)
    cancel = BooleanField(null=False, default=False)
    
    def content(self):
        if self.cancel is True:
            return mark_safe(
                f'<s>{format(self.nature_of_content)}</s>'
            )
        else:
            return self.nature_of_content

    def recipient_render(self):
        if self.cancel is True:
            return mark_safe(
                f'<s>{format(self.recipient)}</s>'
            )
        else:
            return self.recipient

    def save(self, *args, **kwargs):
        if not self.transmittal_number:
            year = datetime.now().year
            max_number = ExternalCommunication.objects.filter(transmittal_number__endswith=str(year)).aggregate(Max('transmittal_number'))
        
            if max_number['transmittal_number__max']:
                max_number = max_number['transmittal_number__max']
            else:
                max_number = f"ORMM-0-{year}"

            number = int(re.search(r"\-(\d+)\-", max_number).group(1)) + 1

            self.transmittal_number = f"ORMM-{number:03d}-{year}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.transmittal_number

