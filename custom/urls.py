from django.urls import path

from . import views

urlpatterns = [
    path('export/users', views.export_users, name='export/users')
]
