from django.contrib.gis.db.models import (
    DateTimeField,
    DO_NOTHING,
    FloatField,
    ForeignKey,
    Index,
    Model,
    OneToOneField,
    PROTECT,
    PointField,
    PositiveIntegerField,
    PositiveSmallIntegerField,
    SET_NULL,
    SmallIntegerField,
    TextField,
    UniqueConstraint
)

from custom.models import User
from fleet.models.equipment import Equipment


class EquipmentLocation(Model):
    equipment = ForeignKey(Equipment, on_delete=PROTECT)
    geom = PointField(srid=4326)
    heading = PositiveSmallIntegerField(null=True, blank=True)
    satellites = PositiveSmallIntegerField(null=True, blank=True)
    speed = PositiveSmallIntegerField(null=True, blank=True)
    time_stamp = DateTimeField(auto_now_add=True)
    user = ForeignKey(User, null=True, blank=True, on_delete=SET_NULL)

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
    geom = PointField(srid=4326)
    time_stamp = DateTimeField()
    ts_begin = DateTimeField()
    ts_end = DateTimeField()

    class Meta:
        db_table = 'location_haulingequipment'
        managed = False


class LoadingEquipment(Model):
    equipment = ForeignKey(Equipment, on_delete=DO_NOTHING)
    geom = PointField(srid=4326)
    time_stamp = DateTimeField()
    ts_begin = DateTimeField()
    ts_end = DateTimeField()

    class Meta:
        db_table = 'location_loadingequipment'
        managed = False


class ManilaGpsWebsocketData(Model):
    alt = SmallIntegerField(blank=True, null=True)
    battery_level = PositiveSmallIntegerField(blank=True, null=True)
    call_time = DateTimeField(blank=True, null=True)
    connection_status = TextField(blank=True, null=True)
    equipment = OneToOneField(Equipment, on_delete=PROTECT)
    geom = PointField(blank=True, null=True, srid=4326)
    heading = PositiveSmallIntegerField(blank=True, null=True)
    last_blocked = DateTimeField(blank=True, null=True)
    last_success = DateTimeField(blank=True, null=True)
    lat = FloatField(blank=True, null=True)
    lon = FloatField(blank=True, null=True)
    movement_status = TextField(blank=True, null=True)
    network_name = TextField(blank=True, null=True)
    signal_level = PositiveSmallIntegerField(blank=True, null=True)
    speed = PositiveSmallIntegerField(blank=True, null=True)
    tracker_id = PositiveIntegerField()
    update_battery = DateTimeField(blank=True, null=True)
    update_gps = DateTimeField(blank=True, null=True)
    update_gsm = DateTimeField(blank=True, null=True)
    update_last = DateTimeField(blank=True, null=True)

