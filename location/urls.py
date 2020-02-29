from django.urls import path

from . import views

app_name = 'location'
urlpatterns = [
    path('data-export/cluster',
         views.export_cluster2,
         name='data-export-cluster'),
    path('data-export/cluster-str',
         views.export_cluster_str,
         name='data-export-cluster-str'),
    path('export/cluster', views.export_cluster, name='export-cluster'),
]
