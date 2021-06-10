from django.db.models import Model, PositiveSmallIntegerField


class TrackedExcavator(Model):
    fleet_number = PositiveSmallIntegerField(unique=True)

    class Meta:
        ordering = ['fleet_number']

    def __str__(self):
        return f'TX-{self.fleet_number}'
