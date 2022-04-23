from os import environ

from custom.functions import send_sms, sender_registered

phone_number = environ['SMS_1_NUMBER']
if sender_registered(phone_number):
    text = f'Hello registered number {phone_number}.\nNothing to do here yet.'
else:
    text = f'Hello unregistered number {phone_number}.\nNothing to do here yet.'
send_sms(phone_number, text)
