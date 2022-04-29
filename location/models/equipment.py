from django.contrib.gis.db.models import (
    DateTimeField,
    ForeignKey,
    Model,
    PROTECT,
    PointField,
    SET_NULL
)

from custom.models import User
from fleet.models.equipment import Equipment


class EquipmentLocation(Model):
    equipment = ForeignKey(Equipment, on_delete=PROTECT)
    time_stamp = DateTimeField(auto_now_add=True)
    user = ForeignKey(User, null=True, blank=True, on_delete=SET_NULL)
    geom = PointField(srid=4326)
