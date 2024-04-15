from django_admin_multiple_choice_list_filter.list_filters import MultipleChoiceListFilter
from .functions import contractor_equipment_classes, contractor_with_equipment


class ProviderEquipmentRegistryClassFilter(MultipleChoiceListFilter):
    title = 'Equipment Class'
    parameter_name = 'x_equipment_class__in'

    def lookups(self, request, model_admin):
        equipment_classes = contractor_equipment_classes()
        equipment_class_choices = []
        for equipment_class in equipment_classes:
            equipment_class_choices.append((equipment_class, equipment_class))
        return tuple(equipment_class_choices)


class ProviderEquipmentRegistryProviderFilter(MultipleChoiceListFilter):
    title = 'Contractor'
    parameter_name = 'x_contractor__in'

    def lookups(self, request, model_admin):
        contractors = contractor_with_equipment()
        contractor_choices = []
        for contractor in contractors:
            contractor_choices.append((contractor, contractor))
        return tuple(contractor_choices)

