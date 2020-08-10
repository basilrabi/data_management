from django.core.exceptions import ValidationError

from .sample import (
    DrillCoreSample, Laboratory, MiningSample, ShipmentDischargeAssay
)

# pylint: disable=no-member

class AcquiredMiningSample(MiningSample):
    class Meta:
        proxy = True


class ChinaShipmentAssay(ShipmentDischargeAssay):

    def clean(self):
        super().clean()
        if self.dmt and self.wmt:
            if self.dmt >= self.wmt:
                raise ValidationError('DTM cannot be higher than WMT.')


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
