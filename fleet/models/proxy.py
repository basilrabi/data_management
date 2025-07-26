from .maintenance import EquipmentBreakdown


class EquipmentBreakdownReport(EquipmentBreakdown):
    class Meta:
        proxy = True
