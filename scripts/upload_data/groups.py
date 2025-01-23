from csv import DictReader
from django.contrib.auth.models import Group, Permission
from os import environ
from sys import exit

with open(environ['datadir']+ '/groups.csv', newline='') as csvfile:
    reader = DictReader(csvfile, fieldnames=['name'])
    for row in reader:
        group = Group(name=row['name'])
        try:
            group.clean()
            group.save()
            print(f'Group {group.name} saved.', flush=True)
        except KeyboardInterrupt:
            print('\nUploading interrupted.')
            exit(1)
        except Exception as e:
            print(f'Group {group.name} was not saved.', flush=True)
            print(e, flush=True)
            exit(1)

with open(environ['datadir']+ '/group_permission.csv', newline='') as csvfile:
    reader = DictReader(csvfile, fieldnames=['group', 'permission'])
    for row in reader:
        group = Group.objects.get(name=row['group'])
        for permission in Permission.objects.filter(codename=row['permission']):
            try:
                group.permissions.add(permission)
                print(f'Permission `{permission.name}` assigned to Group `{group.name}`.', flush=True)
            except KeyboardInterrupt:
                print('\nUploading interrupted.')
                exit(1)
            except Exception as e:
                print(f"Permission `{row['permission']}` not assigned to Group `{group.name}`.", flush=True)
                print(e, flush=True)

