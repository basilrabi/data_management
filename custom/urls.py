from django.urls import path

from . import views

urlpatterns = [
    path('export/group-permissions',
         views.export_permission_group,
         name='export-group-permissions'),
    path('export/groups', views.export_groups, name='export-groups'),
    path('export/user-permissions',
         views.export_permission_user,
         name='export-user-permissions'),
    path('export/users', views.export_users, name='export-users')
]
