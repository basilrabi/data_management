from datetime import datetime

def filepath(instance, filename):
    class_name = instance.__class__.__name__
    date_string = instance.date_registered.strftime("%Y-%m-%d")
    filename = f"camp_admin/{class_name}/{instance.equipment.equipment}/{date_string}.pdf"
    return filename