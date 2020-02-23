from django.urls import path

from . import views

app_name = 'custom'
urlpatterns = [
     path('export', views.export, name='export'),
     path('export/group-permissions',
          views.export_group_permission,
          name='export-group-permissions'),
     path('export/groups', views.export_groups, name='export-groups'),
     path('export/user-groups',
          views.export_user_group,
          name='export-user-groups'),
     path('export/user-permissions',
          views.export_user_permission,
          name='export-user-permissions'),
     path('export/users', views.export_users, name='export-users')
]
