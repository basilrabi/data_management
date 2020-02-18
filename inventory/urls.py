from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('export/block', views.export_block, name='export-block'),
    path('export/clustered-block',
         views.export_clustered_block,
         name='export-clustered-block')
]
