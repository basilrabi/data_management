from django.db.models import (
    CharField,
    DateTimeField,
    F,
    ForeignKey,
    Model,
    PositiveIntegerField,
    PositiveSmallIntegerField,
    PROTECT,
    TextField
)

from custom.models import Classification, User
from fleet.models.equipment import InhouseEquipment


class BreakdownStatus(Classification):
    class Meta:
        ordering = [F('name').asc()]
        verbose_name_plural = 'Breakdown statuses'


class CauseCode(Classification):
    class Meta:
        ordering = [F('name').asc()]


class ComponentCode(Classification):
    class Meta:
        ordering = [F('name').asc()]


class DamageCode(Classification):
    class Meta:
        ordering = [F('name').asc()]


class EquipmentBreakdown(Model):
    """
    Breakdown instance of an equipment.
    """
    breakdown_end = DateTimeField(blank=True, null=True)
    description = TextField(blank=True, null=True)
    equipment = ForeignKey(InhouseEquipment, on_delete=PROTECT)
    maintenance_order = PositiveIntegerField(blank=True, null=True, unique=True)
    mo_created_on = DateTimeField(blank=True, null=True)
    mo_creator = ForeignKey(User, blank=True, null=True, on_delete=PROTECT, related_name='maintenance_order')
    released_by = ForeignKey(User, blank=True, null=True, on_delete=PROTECT, related_name='equipment_breakdown_release')
    reported_on = DateTimeField(auto_now_add=True)
    reporter = ForeignKey(User, blank=True, null=True, on_delete=PROTECT, related_name='equipment_breakdown_report')
    status = ForeignKey('BreakdownStatus', blank=True, null=True, on_delete=PROTECT)

    # Auto-computed field used for multiple choice filters
    x_equipment_class = CharField(blank=True, max_length=40, null=True)


class MaintenanceOperation(Model):
    """
    Maintenance operation done on an equipment breakdown.
    """
    cause = ForeignKey('CauseCode', blank=True, null=True, on_delete=PROTECT)
    component = ForeignKey('ComponentCode', blank=True, null=True, on_delete=PROTECT)
    damage = ForeignKey('DamageCode', blank=True, null=True, on_delete=PROTECT)
    description = TextField(blank=True, null=True)
    maintenance_order = ForeignKey('EquipmentBreakdown', on_delete=PROTECT)
    operation_start = DateTimeField(blank=True, null=True)
    operation_end = DateTimeField(blank=True, null=True)
    part_group = ForeignKey('PartGroup', blank=True, null=True, on_delete=PROTECT)
    supervisor = ForeignKey(User, blank=True, null=True, on_delete=PROTECT)


class MaintenanceTask(Model):
    """
    Task done for a MaintenanceOperation.
    """
    operation = ForeignKey('MaintenanceOperation', on_delete=PROTECT)
    repair_made = TextField(blank=True, null=True)
    task_end = DateTimeField(blank=True, null=True)
    task_start = DateTimeField(blank=True, null=True)


class MaintenanceTaskManpower(Model):
    """
    Manpower complement of a maintenance task
    """
    manpower_count = PositiveSmallIntegerField(blank=True, null=True)
    task = ForeignKey('MaintenanceTask', on_delete=PROTECT)
    work_center = ForeignKey('WorkCenter', on_delete=PROTECT)


class PartGroup(Classification):
    class Meta:
        ordering = [F('name').asc()]


class WorkCenter(Classification):
    class Meta:
        ordering = [F('name').asc()]

