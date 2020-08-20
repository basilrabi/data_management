from django.urls import path

from . import views

app_name = 'sampling'
urlpatterns = [
    path('', views.index, name='index'),
    path('assay/<slug:name>',
         views.assay_certificate,
         name='assay-certificate'),
]
