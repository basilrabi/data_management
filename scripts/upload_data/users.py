from csv import DictReader
from django.contrib.auth.models import Group, Permission
from sys import exit

from custom.models import User

with open('data/users.csv', newline='') as csvfile:
    reader = DictReader(csvfile, fieldnames=[
        'birth_date',
        'email',
        'first_name',
        'username',
        'is_active',
        'is_staff',
        'is_superuser',
        'last_name',
        'middle_name',
        'password',
        'sex',
        'uid',
        'vnc_id'
    ])
    for row in reader:
        user = User(
            birth_date=row['birth_date'] or None,
            email=row['email'],
            first_name=row['first_name'],
            is_active=row['is_active'],
            is_staff=row['is_staff'],
            is_superuser=row['is_superuser'],
            last_name=row['last_name'],
            middle_name=row['middle_name'],
            password=row['password'],
            sex=row['sex'] or None,
            username=row['username'],
            uid=row['uid'] or None,
            vnc_id=row['vnc_id'] or None
        )
        try:
            user.clean()
            user.save()
            print(f'User {user.username} saved.', flush=True)
        except KeyboardInterrupt:
            print('\nUploading interrupted.')
            exit(1)
        except Exception as e:
            print(f'Error: User {user.username} was not saved.', flush=True)
            print(e, flush=True)

with open('data/user_group.csv', newline='') as csvfile:
    reader = DictReader(csvfile, fieldnames=['user', 'group'])
    for row in reader:
        user = User.objects.get(username=row['user'])
        group = Group.objects.get(name=row['group'])
        try:
            user.groups.add(group)
            print(f'Added User `{user.username}` to Group `{group.name}`.', flush=True)
        except KeyboardInterrupt:
            print('\nUploading interrupted.', flush=True)
            exit(1)
        except Exception as e:
            print(f'Error: User `{user.username}` was not assigned to Group `{group.name}`.', flush=True)
            print(e, flush=True)

with open('data/user_permission.csv', newline='') as csvfile:
    reader = DictReader(csvfile, fieldnames=['user', 'permission'])
    for row in reader:
        user = User.objects.get(username=row['user'])
        permission = Permission.objects.get(codename=row['permission'])
        try:
            user.user_permissions.add(permission)
            print(f'Added Permission `{permission.name}` to User `{user.username}`.', flush=True)
        except KeyboardInterrupt:
            print('\nUploading interrupted.', flush=True)
            exit(1)
        except Exception as e:
            print(f'Error: Permission `{permission.name}` was not assigned to User `{user.username}`', flush=True)
            print(e, flush=True)
            exit(1)

