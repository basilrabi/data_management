from datetime import timedelta
from django.db.models import (
    DateField,
    FileField,   
    ForeignKey,
    Model,
    OneToOneField,
    PROTECT
)

from fleet.models.equipment import Equipment
from .functions import filepath


class Insurance(Model):
    date_registered = DateField(null=True, blank=False)
    date_expiry = DateField(null=True, blank=True, help_text="Leave blank if expiry is exactly a year from registration")
    registration_scan = FileField(upload_to=filepath, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk and self.date_registered:
            if self.date_expiry is None:
                self.date_expiry = self.date_registered + timedelta(days=365)
        super().save(*args, **kwargs)


class CTPL(Insurance):
    """
    CTPL = Compulsory Third Party Liability Insurance
    """
    equipment = ForeignKey('VehicularInsurance', on_delete=PROTECT)
    

class Comprehensive(Insurance):
    equipment = ForeignKey('VehicularInsurance', on_delete=PROTECT)


class Floater(Insurance):
    equipment = ForeignKey('VehicularInsurance', on_delete=PROTECT)


class VehicularInsurance(Model):
    equipment = OneToOneField(Equipment, on_delete=PROTECT, primary_key=True)