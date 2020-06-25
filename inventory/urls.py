from django.urls import path

from . import views

app_name = 'inventory'
urlpatterns = [
     path('', views.index, name='index'),
     path('data-export/clustered-block',
          views.export_clustered_block2,
          name='data-export-clustered-block'),
     path('data-export/scheduled-block',
          views.scheduled_block,
          name='data-export-scheduled-block'),
     path('export/clustered-block',
          views.export_clustered_block,
          name='export-clustered-block')
]
