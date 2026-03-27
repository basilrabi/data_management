from django.db.models import Manager


class InhouseEquipmentManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(owner__name='TMC')


class ProviderEquipmentManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(owner__service='Contractor')

