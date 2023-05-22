from django.db.models import (
    CharField,
    DateField, 
    FileField,
    Max, 
    Model, 
    TextField
)
from datetime import datetime
import re

from .functions import filepath


class ExternalCommunication(Model):
    transmittal_number = CharField(max_length=13, null=False, blank=True, primary_key=True)
    date = DateField(null=True, blank=False)
    nature_of_content = TextField(max_length=99, null=True, blank=True)
    receiving_copy = FileField(upload_to=filepath,null=True, blank=True)

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

