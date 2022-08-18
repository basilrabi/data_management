from django.core.management.base import BaseCommand
from os import environ

from custom.functions import get_sender, send_sms, sms_response
from custom.models import Log


class Command(BaseCommand):
    def handle(self, *args, **options):
        phone_number = environ['SMS_1_NUMBER']
        parts = int(environ['DECODED_PARTS'])
        if parts == 0:
            sms = environ["SMS_1_TEXT"]
        else:
            sms = ''
            for i in range(1, parts + 1):
                varname = f'DECODED_{i}_TEXT'
                if varname in environ:
                    sms += environ[varname]
        if phone_number[:4] != '+639':
            Log(log=f'Ignored SMS from {phone_number}: {sms}').save()
            return
        sender = get_sender(phone_number)
        if sender:
            Log(log=f'Received SMS from {sender}: {sms}').save()
            text = sms_response(sms, sender)
        else:
            Log(log=f'Received SMS from {phone_number}: {sms}').save()
            text = 'Hello, your number is unrecognized. Please have your phone number registered first.'
        send_sms(phone_number, text)
        return
