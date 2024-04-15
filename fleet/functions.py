from .models.equipment import ProviderEquipment

def contractor_equipment_classes() -> list[str]:
    """
    Returns the list of equipment classes registered from contractors.
    """
    equipment_classes = set(
        ProviderEquipment.objects \
            .values_list('equipment_class__name', flat=True) \
            .distinct()
    )
    choices = list(filter(None, equipment_classes))
    choices.sort()
    return choices

def contractor_with_equipment() -> list[str]:
    """
    Returns the list of contractors with registered equipment.
    """
    contractors = set(
        ProviderEquipment.objects \
            .values_list('owner__name', flat=True) \
            .distinct()
    )
    choices = list(filter(None, contractors))
    choices.sort()
    return choices

