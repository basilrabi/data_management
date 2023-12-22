from datetime import datetime
import re

def filepath_shipmentimages(instance, filename):
    return f"shipment/draftsurvey/{instance.shipment}.pdf"

def filepath_shipmentvideo(instance, filename):
    return f"shipment/draftsurvey/{instance.shipment}.mp4"
