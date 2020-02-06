from django.contrib.auth.models import User

from .functions import export_csv

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
