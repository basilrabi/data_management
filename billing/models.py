from os import name
from django.db import models


# Create your models here.

def filepath(instance, filename):
    filename = f"{instance.contractor}-{instance.purpose}-{instance.start_date}{instance.specification}.pdf"
    return f"billing/billing_scans/{instance.contractor}/{instance.purpose}/{filename}"

class BillingTracker(models.Model):

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

    contractor = models.CharField(max_length=32, choices=contractor_choices, null=True, blank=False)
    purpose = models.CharField(max_length=32, choices=purpose_choices, null=True, blank=False)
    specification = models.CharField(max_length=50, null=True, blank=True)
    start_date = models.DateField(null = True, blank=False)
    end_date = models.DateField(null = True, blank=False)
    amount = models.FloatField(blank=False)
    tonnage = models.FloatField(null=True, blank=True)
    operating_hours = models.FloatField(null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True)
    invoice_number = models.CharField(max_length=32, null=True, blank=True)
    fileup = models.FileField(upload_to=filepath, null=True, blank=True)


class BillingAddOn(models.Model):
    sent_to_choices = (
        ('Sir Jun', 'Sir Jun'),
        ('Accounting/Advance', 'Accounting/Advance'),
        ('Mines', 'Mines'),
        ('Envi', 'Envi'),
        ('Others', 'Others')
        )

    billing = models.ForeignKey(BillingTracker, null=True, on_delete=models.CASCADE)
    received_from = models.CharField(max_length=32, choices=sent_to_choices, null=True, blank=True)
    received_by = models.DateTimeField(null = True, blank=True)
    notes_received = models.TextField(null=True, blank=True)
    sent_to = models.CharField(max_length=32, choices=sent_to_choices, null=True, blank=True)
    sent_by = models.DateTimeField(null=True, blank=True)
    notes_sent = models.TextField(null=True, blank=True)
