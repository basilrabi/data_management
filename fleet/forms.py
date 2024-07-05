from django.forms import ModelForm
from .models.equipment import ProviderEquipmentRegistry


class ProviderEquipmentRegistryAdminForm(ModelForm):
    def full_clean(self):
        super().full_clean()
        duplicate_safety = ProviderEquipmentRegistry.objects.filter(safety_inspection_id=self.instance.safety_inspection_id)
        if self.instance.id:
            duplicate = duplicate_safety.exclude(id=self.instance.id)
            if duplicate.exists():
                self.add_error('safety_inspection_id', f'Similar safety inspection id duplicated in {duplicate[0]}.')
        else:
            if duplicate_safety.exists():
                self.add_error('safety_inspection_id', f'Similar safety inspection id duplicated in {duplicate_safety[0]}.')

