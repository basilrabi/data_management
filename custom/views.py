from django.contrib.auth.models import Group, User

from .functions import export_csv

def export_group_permission(request):
    rows = ([
        str(group.name),
        str(permission.codename)
    ] for group in Group.objects.all() for permission in group.permissions.all())
    return export_csv(rows, 'group_permission')

def export_groups(request):
    rows = ([
        str(group.name)
    ] for group in Group.objects.all())
    return export_csv(rows, 'groups')

def export_user_group(request):
    rows = ([
        str(user.get_username()),
        str(group.name)
    ] for user in User.objects.all() for group in user.groups.all())
    return export_csv(rows, 'user_group')

def export_user_permission(request):
    rows = ([
        str(user.get_username()),
        str(permission.codename)
    ] for user in User.objects.all() for permission in user.user_permissions.all())
    return export_csv(rows, 'user_permission')

def export_users(request):
    rows = ([
        str(user.get_username()),
        str(user.first_name),
        str(user.last_name),
        str(user.email),
        str(user.password),
        str(user.is_staff),
        str(user.is_active),
        str(user.is_superuser)
    ] for user in User.objects.all())
    return export_csv(rows, 'users')
