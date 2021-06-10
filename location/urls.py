from django.urls import path

from .views import (
     export_cluster,
     export_cluster_dxf_for_survey,
     export_cluster_str,
     export_cluster_str_for_survey
)

app_name = 'location'
urlpatterns = [
     path('data-export/cluster',
          export_cluster,
          name='data-export-cluster'),
     path('data-export/cluster-dxf-survey',
          export_cluster_dxf_for_survey,
          name='data-export-cluster-dxf-survey'),
     path('data-export/cluster-str',
          export_cluster_str,
          name='data-export-cluster-str'),
     path('data-export/cluster-str-survey',
          export_cluster_str_for_survey,
          name='data-export-cluster-str-survey'),
]
