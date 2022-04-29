from ast import Eq
from django.contrib.gis.db.models import (
    DateTimeField,
    ForeignKey,
    Model,
    PROTECT,
    PointField
)

from fleet.models.equipment import Equipment


class EquipmentLocation(Model):
    equipment = ForeignKey(Equipment, on_delete=PROTECT)
    time_stamp = DateTimeField(auto_now_add=True)
    geom = PointField(srid=4326)
