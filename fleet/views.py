from custom.functions import export_sql

def data_export_provider_equipment_registry(request):
    """
    CSV view of provider equipment registry.
    """
    return export_sql('export_providerequipmentregistry', 'equipment_registry')

