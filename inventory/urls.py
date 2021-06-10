from django.urls import path

from .views import export_clustered_block, index, scheduled_block

app_name = 'inventory'
urlpatterns = [
     path('', index, name='index'),
     path('data-export/clustered-block',
          export_clustered_block,
          name='data-export-clustered-block'),
     path('data-export/scheduled-block',
          scheduled_block,
          name='data-export-scheduled-block')
]
