from datetime import date,timedelta
from camp_admin import models
from django.core.mail import EmailMessage, send_mail
from data_management.local import email_address

def filepath(instance, filename):
    class_name = instance.__class__.__name__
    date_string = instance.date_registered.strftime("%Y-%m-%d")
    filename = f"camp_admin/{class_name}/{instance.equipment.equipment}/{date_string}.pdf"
    return filename

def get_expiring():
    expiring = models.Insurance.objects.filter(date_expiry__range=[date.today(), date.today()+timedelta(30)]).values_list('date_registered','date_expiry',named=True)
    subject = "Insurance Expiry Notice"
    message = str(expiring)
    send_mail(
        "EXPIRING INSURANCES",
        message,
        email_address,
        ["john.velonta@tmc.nickelasia.com"],
        fail_silently=False,
        )
    return(expiring)