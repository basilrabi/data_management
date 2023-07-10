from django.db.models import (
    CASCADE,
    CharField,
    DateField,
    DateTimeField,
    FileField,
    FloatField,
    ForeignKey,
    Model,
    PROTECT,
    TextField
)
from datetime import datetime
import calendar

from organization.models import Organization

def filepath(instance, filename):
    filename = f"{instance.contractor}-{instance.purpose}-{instance.start_date}{instance.specification}.pdf"
    return f"billing/billing_scans/{instance.contractor}/{instance.purpose}/{filename}"


class BillingAddOn(Model):

    sent_to_choices = (
        ('Sir Jun', 'Sir Jun'),
        ('Accounting/Advance', 'Accounting/Advance'),
        ('Mines', 'Mines'),
        ('Envi', 'Envi'),
        ('Others', 'Others')
    )

    billing = ForeignKey('BillingTracker', null=True, on_delete=CASCADE)
    received_from = CharField(
        max_length=32, choices=sent_to_choices, null=True, blank=True
    )
    received_by = DateTimeField(null = True, blank=True)
    notes_received = TextField(null=True, blank=True)
    sent_to = CharField(
        max_length=32, choices=sent_to_choices, null=True, blank=True
    )
    sent_by = DateTimeField(null=True, blank=True)
    notes_sent = TextField(null=True, blank=True)


class BillingTracker(Model):

    contractor_choices = (
        ('CKDI', 'CKDI'),
        ('TRGC', 'TRGC'),
        ('SDMC', 'SDMC'),
        ('HPK', 'HPK'),
        ('NB', 'NICKELBASE'),
        ('POL', 'POLARIS'),
        ('ETER', 'ETER')
    )

    purpose_choices = (
        ('SHIP','Shipment'),
        ('REN','Rental'),
        ('LIM','Limonite'),
        ('ENV','Envi')
    )

    contractor = CharField(
        max_length=32, choices=contractor_choices, null=True, blank=False
    )
    purpose = CharField(
        max_length=32, choices=purpose_choices, null=True, blank=False
    )
    specification = CharField(max_length=50, null=True, blank=True)
    start_date = DateField(null = True, blank=False)
    end_date = DateField(null = True, blank=False)
    amount = FloatField(blank=False)
    tonnage = FloatField(null=True, blank=True)
    operating_hours = FloatField(null=True, blank=True)
    last_update = DateTimeField(auto_now=True)
    invoice_number = CharField(max_length=32, null=True, blank=True)
    fileup = FileField(upload_to=filepath, null=True, blank=True)


class CMBilling(Model):
    
    month_choices = [(str(i), calendar.month_name[i]) for i in range(1,13)]
    half = [('1','1st'),('2','2nd')]
    year_now = datetime.now().year

    contractor = ForeignKey(Organization, on_delete = PROTECT, null=True)
    billing_year = CharField(max_length=4, default=year_now, null=True, blank=False)
    month = CharField(max_length=9, choices=month_choices, default='1', null=True, blank=False)
    half = CharField(max_length=3, choices=half, default='1', null=True, blank=False)
    amount = FloatField(null=True, blank=False)
    tonnage = FloatField(null=True, blank=False)
    last_update = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contract Mining Billing"
        verbose_name_plural = "Contract Mining Billings"