from django.apps import AppConfig


class CustomConfig(AppConfig):
    name = 'custom'

    def ready(self):
        from . import signals
