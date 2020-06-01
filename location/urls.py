from django.urls import path

from . import views

app_name = 'location'
urlpatterns = [
     path('data-export/cluster',
          views.export_cluster2,
          name='data-export-cluster'),
     path('data-export/cluster-dxf-survey',
          views.export_cluster_dxf_for_survey,
          name='data-export-cluster-dxf-survey'),
     path('data-export/cluster-str',
          views.export_cluster_str,
          name='data-export-cluster-str'),
     path('data-export/cluster-str-survey',
          views.export_cluster_str_for_survey,
          name='data-export-cluster-str-survey'),
     path('export/cluster', views.export_cluster, name='export-cluster'),
     path('export/drillhole', views.export_drillhole, name='export-drillhole'),
]
