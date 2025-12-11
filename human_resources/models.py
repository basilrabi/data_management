from datetime import datetime
from django.db.models import (
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    FileField,
    ForeignKey,
    Max,
    Model,
    PROTECT,
    TextField
)
from django.utils.html import mark_safe
import re

from .functions import filepath, filepath_extincomingcomm, filepath_original
from organization.models import OrganizationUnit


class OutgoingCommunication(Model):
    """
    Digital log of outgoing communication from HRD.
    """

    transmittal_number = CharField(max_length=13, null=False, blank=True, primary_key=True)
    date = DateField(null=True, blank=False)
    nature_of_content = TextField(max_length=99, null=True, blank=True)
    recipient = CharField(max_length=30, null=False, blank=False, default='')
    original_copy = FileField(upload_to=filepath_original,null=True, blank=True)
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
            if not self.date:
                year = datetime.now().year
            else:
                year = self.date.year

            max_number = OutgoingCommunication.objects.filter(transmittal_number__endswith=str(year)).aggregate(Max('transmittal_number'))

            if max_number['transmittal_number__max']:
                max_number = max_number['transmittal_number__max']
            else:
                max_number = f"HRD-0-{year}"

            number = int(re.search(r"\-(\d+)\-", max_number).group(1)) + 1
            self.transmittal_number = f"HRD-{number:03d}-{year}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.transmittal_number


class ExternalIncomingCommunication(Model):
    """
    Digital log of incoming communications from external sources
    """

    transmittal_number = CharField(max_length=20, null=False, blank=True, primary_key=True)
    datetime_received = DateTimeField(null=True, blank=False)
    sender = CharField(max_length=99, null=True, blank=False)
    subject = TextField(max_length=499, null=True, blank=False)
    scan = FileField(upload_to=filepath_extincomingcomm, null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.transmittal_number:
            year = datetime.now().year
            month = datetime.now().month
            max_number = ExternalIncomingCommunication.objects.filter(transmittal_number__endswith=str(year)).aggregate(Max('transmittal_number'))

            if max_number['transmittal_number__max']:
                max_number = max_number['transmittal_number__max']
            else:
                max_number = f"HRDRECV-0-{year}"

            number = int(re.search(r"\-(\d+)\-", max_number).group(1)) + 1

            self.transmittal_number = f"HRDRECV-{number:03d}-{year}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.transmittal_number
