# from django.db.models.signals import post_save
# from django.dispatch import receiver

# from .functions import on_transaction_commmit, send_sms
# from .models import TextMessage

# @receiver(post_save, sender=TextMessage)
# @on_transaction_commmit
# def send_text(sender, **kwargs):
#     obj = kwargs['instance']
#     recipient = obj._recipient()
#     if recipient and obj.sms:
#         for number in recipient:
#             send_sms(number, obj.sms)
