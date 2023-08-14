from django.contrib.gis.db.models import (
    DateTimeField,
    DO_NOTHING,
    ForeignKey,
    Index,
    Model,
    PROTECT,
    PointField,
    PositiveSmallIntegerField,
    SET_NULL,
    UniqueConstraint
)

from custom.models import User
from fleet.models.equipment import Equipment


class EquipmentLocation(Model):
    equipment = ForeignKey(Equipment, on_delete=PROTECT)
    time_stamp = DateTimeField(auto_now_add=True)
    heading = PositiveSmallIntegerField(null=True, blank=True)
    satellites = PositiveSmallIntegerField(null=True, blank=True)
    speed = PositiveSmallIntegerField(null=True, blank=True)
    user = ForeignKey(User, null=True, blank=True, on_delete=SET_NULL)
    geom = PointField(srid=4326)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['equipment', 'time_stamp'],
                name='unique_equipment_location_timestamp'
            )
        ]
        indexes = [
            Index(fields=['time_stamp'])
        ]

    def __str__(self) -> str:
        return f'{self.time_stamp} - {self.equipment}'


class HaulingEquipment(Model):
    equipment = ForeignKey(Equipment, on_delete=DO_NOTHING)
    ts_begin = DateTimeField()
    ts_end = DateTimeField()
    time_stamp = DateTimeField()
    geom = PointField(srid=4326)

    class Meta:
        db_table = 'location_haulingequipment'
        managed = False


class LoadingEquipment(Model):
    equipment = ForeignKey(Equipment, on_delete=DO_NOTHING)
    ts_begin = DateTimeField()
    ts_end = DateTimeField()
    time_stamp = DateTimeField()
    geom = PointField(srid=4326)

    class Meta:
        db_table = 'location_loadingequipment'
        managed = False

