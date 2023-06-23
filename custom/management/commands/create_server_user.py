from django.core.management.base import BaseCommand
from os import environ
from subprocess import PIPE, run

from custom.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Creates a linux user account for all members of group `server user`.
        """
        users = User.objects.filter(groups__name="server user")
        cmd = ["cat", "/etc/passwd"]
        accounts = run(cmd, stdout=PIPE).stdout.decode("utf-8")
        for user in users:
            if not user.username in accounts:
                cmd = ["useradd",
                       "-c",
                       f"{user.first_name} {user.last_name}",
                       "-p",
                       "taganitomine2023",
                       user.username]
                log = run(cmd, stdout=PIPE).stdout.decode("utf-8")
                Log(log=log).save()
