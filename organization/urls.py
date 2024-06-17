from django.urls import path

from .views import index

app_name = 'organization'

urlpatterns = [
    path('', index, name='index')
]

