from django.urls import path

from .views import assay_certificate, index

app_name = 'sampling'
urlpatterns = [
    path('', index, name='index'),
    path('assay/<slug:name>',
         assay_certificate,
         name='assay-certificate'),
]
