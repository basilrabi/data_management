from django.urls import path

from .views import data_export_provider_equipment_registry

app_name = 'fleet'
urlpatterns = [
    path('data-export/provider-equipment-registry',
         data_export_provider_equipment_registry,
         name='data-export-provider-equipment-registry')
]

