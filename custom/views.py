import os

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.shortcuts import render

from .functions import export_csv

def export(request):
    context = {
        'db_host': settings.DB_HOST,
        'db_port': settings.DB_PORT,
        'db_name': settings.DB_NAME,
        'geology': os.environ['DATA_MANAGEMENT_GEOLOGY'],
        'gradecontrol': os.environ['DATA_MANAGEMENT_GRADECONTROL'],
        'survey': os.environ['DATA_MANAGEMENT_SURVEY']
    }
    return render(request, 'custom/export.html', context=context)

def export_group_permission(request):
    rows = ([
        str(group.name),
        str(permission.codename)
    ] for group in Group.objects.all().order_by('name') for permission in group.permissions.all().order_by('codename'))
    return export_csv(rows, 'group_permission')

def export_groups(request):
    rows = ([
        str(group.name)
    ] for group in Group.objects.all().order_by('name'))
    return export_csv(rows, 'groups')

def export_user_group(request):
    rows = ([
        str(user.get_username()),
        str(group.name)
    ] for user in User.objects.all().order_by('username') for group in user.groups.all().order_by('name'))
    return export_csv(rows, 'user_group')

def export_user_permission(request):
    rows = ([
        str(user.get_username()),
        str(permission.codename)
    ] for user in User.objects.all().order_by('username') for permission in user.user_permissions.all().order_by('codename'))
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
    ] for user in User.objects.all().order_by('username'))
    return export_csv(rows, 'users')
