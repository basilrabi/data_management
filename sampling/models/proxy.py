from .sample import (
    DrillCoreSample, Laboratory, MiningSample, ShipmentDischargeAssay
)

# pylint: disable=no-member

class AcquiredMiningSample(MiningSample):
    class Meta:
        proxy = True


class ChinaShipmentAssay(ShipmentDischargeAssay):
    class Meta:
        proxy = True
        verbose_name = 'China Shipment Discharge Assay'


class DrillCore(DrillCoreSample):
    class Meta:
        proxy = True


class DrillCoreAssay(DrillCoreSample):
    class Meta:
        proxy = True


class MiningSampleAssay(MiningSample):
    class Meta:
        proxy = True


class PamcoShipmentAssay(ShipmentDischargeAssay):

    def save(self, *args, **kwargs):
        self.laboratory = Laboratory.objects.get(name='PAMCO')
        super().save(*args, **kwargs)

    class Meta:
        proxy = True
        verbose_name = 'PAMCO Shipment Discharge Assay'
