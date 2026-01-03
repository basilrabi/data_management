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
    SET_NULL,
    TextField
)
from django.utils.html import mark_safe
import re

from .functions import filepath, filepath_extincomingcomm, filepath_original, filepath_letter_original, filepath_letter_receiving, filepath_policies
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
                max_number = f"HRD-RECV-0-{year}"

            number = int(re.search(r"\-(\d+)\-", max_number).group(1)) + 1

            self.transmittal_number = f"HRD-RECV-{number:03d}-{year}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.transmittal_number


class Letter(Model):
    """
    Digital log of outgoing letters from HRD. This is different from Memorandums (Outgoing Communications).
    """

    transmittal_number = CharField(max_length=20, null=False, blank=True, primary_key=True)
    date = DateField(null=True, blank=False)
    nature_of_content = TextField(max_length=99, null=True, blank=True)
    recipient = CharField(max_length=30, null=False, blank=False, default='')
    original_copy = FileField(upload_to=filepath_letter_original,null=True, blank=True)
    receiving_copy = FileField(upload_to=filepath_letter_receiving,null=True, blank=True)
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

            max_number = Letter.objects.filter(transmittal_number__endswith=str(year)).aggregate(Max('transmittal_number'))

            if max_number['transmittal_number__max']:
                max_number = max_number['transmittal_number__max']
            else:
                max_number = f"HRD-LR-0-{year}"

            number = int(re.search(r"\-(\d+)\-", max_number).group(1)) + 1
            self.transmittal_number = f"HRD-LR-{number:03d}-{year}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.transmittal_number
    

class PoliciesAndGuideline(Model):
    transmittal_number = CharField(max_length=20, null=False, blank=True, primary_key=True)
    date = DateField(null=True, blank=False)
    nature_of_content = TextField(max_length=99, null=True, blank=False)
    concerned_personnel = CharField(max_length=99, null=True, blank=True)
    date_of_effectivity = DateField(null=True, blank=False)
    date_of_expiry = DateField(null=True, blank=True)
    signed_copy = FileField(upload_to='policies/', null=True, blank=True)
    
    update_existing = ForeignKey(
        'self', 
        on_delete=SET_NULL, 
        null=True, 
        blank=True, 
        related_name='updated_by',
        verbose_name="Update Existing",
        help_text="Select the existing policy that this entry updates."
    )
    
    cancel = BooleanField(null=False, default=False)

    def content(self):
        if self.cancel is True:
            return mark_safe(f'<s>{format(self.nature_of_content)}</s>')
        return self.nature_of_content

    def recipient_render(self):
        if self.cancel is True:
            return mark_safe(f'<s>{format(self.concerned_personnel)}</s>')
        return self.concerned_personnel

    def save(self, *args, **kwargs):
        if not self.transmittal_number:
            if not self.date:
                year = datetime.now().year
            else:
                year = self.date.year

            max_number = PoliciesAndGuideline.objects.filter(
                transmittal_number__endswith=str(year)
            ).aggregate(Max('transmittal_number'))

            if max_number['transmittal_number__max']:
                max_str = max_number['transmittal_number__max']
            else:
                max_str = f"HRD-POL-0-{year}"

            match = re.search(r"\-(\d+)\-", max_str)
            if match:
                number = int(match.group(1)) + 1
            else:
                number = 1
                
            self.transmittal_number = f"HRD-POL-{number:03d}-{year}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transmittal_number} - {self.nature_of_content}"