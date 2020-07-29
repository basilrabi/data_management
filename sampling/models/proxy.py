from .sample import DrillCoreSample, MiningSample, ShipmentDischargeAssay


class AcquiredMiningSample(MiningSample):
    class Meta:
        proxy = True


class ChinaShipmentAssay(ShipmentDischargeAssay):
    class Meta:
        proxy = True


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
    class Meta:
        proxy = True
        verbose_name = 'PAMCO Shipment Assay'
