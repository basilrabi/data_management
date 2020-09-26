import csv
import sys
from django.contrib.auth.models import Group, Permission

with open('data/groups.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['name'])
    for row in reader:
        group = Group(name=row['name'])
        try:
            group.clean()
            group.save()
            print(f'Group {group.name} saved.', flush=True)
        except KeyboardInterrupt:
            print('\nUploading interrupted.')
            sys.exit(1)
        except Exception as e:
            print(f'Group {group.name} was not saved.', flush=True)
            print(e, flush=True)
            sys.exit(1)

with open('data/group_permission.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['group', 'permission'])
    for row in reader:
        group = Group.objects.get(name=row['group'])
        try:
            permission = Permission.objects.get(codename=row['permission'])
            group.permissions.add(permission)
            print(f'Permission `{permission.name}` assigned to Group `{group.name}`.', flush=True)
        except KeyboardInterrupt:
            print('\nUploading interrupted.')
            sys.exit(1)
        except Exception as e:
            print(f"Permission `{row['permission']}` not assigned to Group `{group.name}`.", flush=True)
            print(e, flush=True)
