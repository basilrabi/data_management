import os

from celery import Celery

from .local import celery_backend_url, celery_broker_url

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'data_management.settings')
app = Celery('data_management', backend=celery_backend_url, broker=celery_broker_url)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
