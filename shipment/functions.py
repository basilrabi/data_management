def filepath_shipment_draftsurvey_receipt(instance, filename):
    return f"shipment/draftsurvey/{instance.shipment}_receipt.pdf"

def filepath_shipmentimages(instance, filename):
    return f"shipment/draftsurvey/{instance.shipment}.pdf"

def filepath_shipmentvideo(instance, filename):
    return f"shipment/draftsurvey/{instance.shipment}.mp4"

