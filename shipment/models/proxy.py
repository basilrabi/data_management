from .dso import Shipment


class FinalShipmentDetail(Shipment):
    class Meta:
        proxy = True
