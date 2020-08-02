from django.urls import path

from . import views

app_name = 'sampling'
urlpatterns = [
    path('assay/<slug:name>',
         views.assay_certificate,
         name='assay-certificate'),
]
