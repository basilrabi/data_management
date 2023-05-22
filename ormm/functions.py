import re

def filepath(instance, filename):
    year = re.search(r"\d{4}", instance.transmittal_number).group(0)
    return f"ORMM/external_communication/{year}/{instance.transmittal_number}.pdf"
