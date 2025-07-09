from django.forms import ModelForm
from .models.equipment import Equipment, ProviderEquipmentRegistry


class EquipmentAdminForm(ModelForm):
    def full_clean(self):
        super().full_clean()
        duplicate_equipment = Equipment.objects.filter(
            equipment_class=self.instance.model.equipment_class,
            fleet_number=self.instance.fleet_number,
            owner=self.instance.owner
        )
        error = f'{self.instance.owner}-{self.instance.model.equipment_class.name}-{self.instance.fleet_number:03d} already exists.'
        error_exists = False
        if self.instance.id:
            duplicate = duplicate_equipment.exclude(id=self.instance.id)
            if duplicate.exists():
                error_exists = True
        else:
            if duplicate_equipment.exists():
                error_exists = True
        if error_exists:
            self.add_error('fleet_number', error)
            self.add_error('model', error)
            self.add_error('owner', error)


class ProviderEquipmentRegistryAdminForm(ModelForm):
    def full_clean(self):
        super().full_clean()
        duplicate_safety = ProviderEquipmentRegistry.objects.filter(
                safety_inspection_id=self.instance.safety_inspection_id,
                year=self.instance.registration_date.year
        )
        if self.instance.id:
            duplicate = duplicate_safety.exclude(id=self.instance.id)
            if duplicate.exists():
                self.add_error('safety_inspection_id', f'Similar safety inspection id duplicated in {duplicate[0]}.')
        else:
            if duplicate_safety.exists():
                self.add_error('safety_inspection_id', f'Similar safety inspection id duplicated in {duplicate_safety[0]}.')

