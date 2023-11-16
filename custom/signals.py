from django.core.mail import send_mass_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .functions import on_transaction_commmit, send_sms
from .models import GroupMail, TextMessage

@receiver(post_save, sender=TextMessage)
@on_transaction_commmit
def send_text(sender, **kwargs):
    obj = kwargs['instance']
    recipient = obj._recipient()
    if recipient and obj.sms:
        for number in recipient:
            send_sms(number, obj.sms)

@receiver(post_save, sender=GroupMail)
@on_transaction_commmit
def send_group_mail(sender, **kwargs):
    obj = kwargs['instance']
    mail_tuple = obj.messages()
    if mail_tuple:
        send_mass_mail(mail_tuple)

