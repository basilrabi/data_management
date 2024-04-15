from django.db.models import Manager


class ProviderEquipmentManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(owner__service='Contractor')

