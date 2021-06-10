from django.urls import path

from .views import index, road

app_name = 'map'
urlpatterns = [
    path('', index, name='index'),
    path('road', road, name='road'),
]
