from django.core.management.base import BaseCommand
from os import environ
from re import sub

from custom.functions import fortune, send_sms, sender_registered
from custom.models import Log


class Command(BaseCommand):
    def handle(self, *args, **options):
        phone_number = environ['SMS_1_NUMBER']
        if phone_number[:4] != '+639':
            Log(log=f'Ignored SMS from {phone_number}: {environ["SMS_1_TEXT"]}').save()
            return
        if sender_registered(phone_number):
            message = sub('\s+', ' ', environ['SMS_1_TEXT']).strip().upper()
            if message == 'FORTUNE':
                text = fortune()
            else:
                text = 'Text pattern unrecognized.'
        else:
            text = 'Hello, your number is unrecognized. Please register your phone number first.'
        send_sms(phone_number, text)
        return
