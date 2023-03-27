from django.urls import path

from .views import (
     export,
     export_group_permission,
     export_groups,
     export_user_group,
     export_user_permission,
     export_user_profession,
     export_users
)

app_name = 'custom'
urlpatterns = [
     path('export', export, name='export'),
     path('export/group-permissions',
          export_group_permission,
          name='export-group-permissions'),
     path('export/groups', export_groups, name='export-groups'),
     path('export/user-groups',
          export_user_group,
          name='export-user-groups'),
     path('export/user-permissions',
          export_user_permission,
          name='export-user-permissions'),
     path('export/user-professions',
          export_user_profession,
          name='export-user-professions'),
     path('export/users', export_users, name='export-users')
]
