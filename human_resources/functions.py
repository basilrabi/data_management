from datetime import datetime
import re

def filepath_extincomingcomm(instance, filename):
    sender_nospace = instance.sender.replace(" ","")
    name = f"{sender_nospace}-{instance.datetime_received}"
    return f"human_resources/ExternalIncomingCommunication/{instance.datetime_received.year}/{instance.datetime_received.month}/{name}.pdf"

def filepath(instance, filename):
    year = re.search(r"\d{4}", instance.transmittal_number).group(0)
    return f"human_resources/OutgoingCommunications/receiving/{year}/{instance.transmittal_number}.pdf"

def filepath_original(instance, filename):
    year = re.search(r"\d{4}", instance.transmittal_number).group(0)
    return f"human_resources/OutgoingCommunications/original/{year}/{instance.transmittal_number}.pdf"
