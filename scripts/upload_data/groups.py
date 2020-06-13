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
            print(f'Group {group.name} saved.')
        except KeyboardInterrupt:
            print('\nUploading interrupted.')
            sys.exit(1)
        except Exception as e:
            print(f'Group {group.name} was not saved.')
            print(e)
            sys.exit(1)
        sys.stdout.flush()
        sys.stderr.flush()

with open('data/group_permission.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['group', 'permission'])
    for row in reader:
        group = Group.objects.get(name=row['group'])
        try:
            permission = Permission.objects.get(codename=row['permission'])
            group.permissions.add(permission)
            print(f'Permission `{permission.name}` assigned to Group `{group.name}`.')
        except KeyboardInterrupt:
            print('\nUploading interrupted.')
            sys.exit(1)
        except Exception as e:
            print(f"Permission `{row['permission']}` not assigned to Group `{group.name}`.")
            print(e)
        sys.stdout.flush()
        sys.stderr.flush()
