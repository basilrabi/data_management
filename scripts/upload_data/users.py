from csv import DictReader
from django.contrib.auth.models import Group, Permission
from sys import exit

from custom.models import User

with open('data/users.csv', newline='') as csvfile:
    reader = DictReader(csvfile, fieldnames=['username',
                                             'first_name',
                                             'middle_name',
                                             'last_name',
                                             'email',
                                             'password',
                                             'is_staff',
                                             'is_active',
                                             'is_superuser'])
    for row in reader:
        user = User(username=row['username'],
                    first_name=row['first_name'],
                    middle_name=row['middle_name'],
                    last_name=row['last_name'],
                    email=row['email'],
                    password=row['password'],
                    is_staff=row['is_staff'],
                    is_active=row['is_active'],
                    is_superuser=row['is_superuser'])
        try:
            user.clean()
            user.save()
            print(f'User {user.username} saved.', flush=True)
        except KeyboardInterrupt:
            print('\nUploading interrupted.')
            exit(1)
        except Exception as e:
            print(f'User {user.username} was not saved.', flush=True)
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
            print(f'User `{user.username}` was not assigned to Group `{group.name}`.', flush=True)
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
            print(f'Permission `{permission.name}` was not assigned to User `{user.username}`', flush=True)
            exit(1)
