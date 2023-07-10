from django.forms import ModelForm
from .models import CMBilling
from organization.models import Organization

class CMBillingForm(ModelForm):
    class Meta:
        model = CMBilling
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contractor'].queryset = Organization.objects.filter(active=True, service='Contractor')
