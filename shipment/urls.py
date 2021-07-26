from django.urls import path

from .views import (
     data_export_laydays,
     data_export_lct_trips,
     data_export_shipments,
     index,
     lay_days_statement_csv,
     lay_days_statement_pdf
)

app_name = 'shipment'
urlpatterns = [
     path('', index, name='index'),
     path('data-export/laydays',
          data_export_laydays,
          name='data-export-laydays'),
     path('data-export/lcttrips',
          data_export_lct_trips,
          name='data-export-lct-trips'),
     path('data-export/shipments',
          data_export_shipments,
          name='data-export-shipments'),
     path('statement/<slug:name>',
          lay_days_statement_pdf,
          name='lay-days-pdf'),
     path('statement-csv/<slug:name>',
          lay_days_statement_csv,
          name='lay-days-csv')
]
