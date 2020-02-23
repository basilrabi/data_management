from django.urls import path

from . import views

app_name = 'shipment'
urlpatterns = [
     path('data-export/laydays',
          views.data_export_laydays,
          name='data-export-laydays'),
     path('data-export/lcttrips',
          views.data_export_lct_trips,
          name='data-export-lct-trips'),
     path('export/laydaysdetail',
          views.export_laydaysdetail,
          name='export-laydayslaydaysdetail'),
     path('export/laydaysstatement',
          views.export_laydaysstatement,
          name='export-laydaysstatement'),
     path('export/lct', views.export_lct, name='export-lct'),
     path('export/lctcontract',
          views.export_lctcontract,
          name='export-lctcontract'),
     path('export/shipment', views.export_shipment, name='export-shipment'),
     path('export/trip', views.export_trip, name='export-trip'),
     path('export/tripdetail',
          views.export_tripdetail,
          name='export-tripdetail'),
     path('export/vessel', views.export_vessel, name='export-vessel'),
     path('statement/<slug:name>',
          views.lay_days_statement_pdf,
          name='lay-days-pdf')
]
