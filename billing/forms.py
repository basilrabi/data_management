from datetime import datetime
from django.forms import ModelForm
from .models import CMBilling, ShipmentBilling

from organization.models import Organization
from shipment.models.dso import LayDaysStatement

class CMBillingForm(ModelForm):
    class Meta:
        model = CMBilling
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contractor'].queryset = Organization.objects.filter(active=True, service='Contractor')


class ShipmentBillingForm(ModelForm):
    class Meta:
        model = ShipmentBilling
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contractor'].queryset = Organization.objects.filter(active=True, service='Contractor')
        self.fields['shipment'].queryset = LayDaysStatement.objects.all().order_by('-id')[:20]