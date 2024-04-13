from django import forms
from .models import MapDocumentControl

class MapDocumentControlForm(forms.ModelForm):
    class Meta:
        model = MapDocumentControl
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['map_type'].queryset = self.fields['map_type'].queryset.order_by('map_type')


