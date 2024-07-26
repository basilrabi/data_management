import os

from celery import Celery

from .local import celery_backend_url, celery_broker_url

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'data_management.settings')
app = Celery('data_management', backend=celery_backend_url, broker=celery_broker_url)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'pull-manilagps-websocket-data': {
        'task': 'location.tasks.pull_manilagps_websocket_data',
        'schedule': 1.0,
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

