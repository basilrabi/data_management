from django.core.management.base import BaseCommand
from os import environ
from re import sub

from custom.functions import fortune, send_sms, sender_registered


class Command(BaseCommand):
    def handle(self, *args, **options):
        phone_number = environ['SMS_1_NUMBER']
        if phone_number[:4] != '+639':
            return
        if sender_registered(phone_number):
            message = sub('\s+', ' ', environ['SMS_1_TEXT']).strip().upper()
            if message == 'FORTUNE':
                send_sms(phone_number, fortune())
                return
            text = f'Hello registered number {phone_number}.'
        else:
            text = f'Hello unregistered number {phone_number}.'
        text += ' Nothing to do here yet but here is a fortune for you. :)\n\n'
        text += fortune()
        send_sms(phone_number, text)
