from django.db import models

class TrackedExcavator(models.Model):
    fleet_number = models.PositiveSmallIntegerField(unique=True)

    class Meta:
        ordering = ['fleet_number']

    def __str__(self):
        return 'TX-{}'.format(self.fleet_number)