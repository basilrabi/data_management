import csv
import sys
from django.contrib.auth.models import User

with open('data/users.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['username',
                                                 'first_name',
                                                 'last_name',
                                                 'email',
                                                 'password',
                                                 'is_staff',
                                                 'is_active',
                                                 'is_superuser'])
    for row in reader:
        user = User(username=row['username'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    email=row['email'],
                    password=row['password'],
                    is_staff=row['is_staff'],
                    is_active=row['is_active'],
                    is_superuser=row['is_superuser'])
        try:
            user.clean()
            user.save()
            print(f'User {user.username} saved.')
        except KeyboardInterrupt:
            print('\nUploading interrupted.')
            break
        except:
            print(f'User {user.username} was not saved.')
        sys.stdout.flush()
        sys.stderr.flush()
