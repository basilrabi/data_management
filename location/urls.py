from django.urls import path

from . import views

urlpatterns = [
    path('export/cluster', views.export_cluster, name='export-cluster'),
]
