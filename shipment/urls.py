from django.urls import path

from . import views

app_name = 'shipment'
urlpatterns = [
     path('', views.index, name='index'),
     path('data-export/laydays',
          views.data_export_laydays,
          name='data-export-laydays'),
     path('data-export/lcttrips',
          views.data_export_lct_trips,
          name='data-export-lct-trips'),
     path('statement/<slug:name>',
          views.lay_days_statement_pdf,
          name='lay-days-pdf'),
     path('statement-csv/<slug:name>',
          views.lay_days_statement_csv,
          name='lay-days-csv')
]
