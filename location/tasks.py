from celery import shared_task
from django.db.models import Subquery
from django.template.loader import get_template
from os import environ, getcwd
from os.path import join
from subprocess import run
from tempfile import TemporaryDirectory

from custom.models import WebsocketListener
from location.models.equipment import ManilaGpsWebsocketData

@shared_task
def pull_manilagps_websocket_data():
    data = ManilaGpsWebsocketData.objects.exclude(id__in=Subquery(WebsocketListener.objects.all().values('id'))).order_by('-call_time').first()
    WebsocketListener(id=data.id).save()
    context = {
        'EQUIPMENT': data.__str__(),
        'ID': str(data.id),
        'HASH': data.equipment.owner.manilagpsapikey_set.first().key,
        'TRACKER_ID': str(data.tracker_id)
    }
    template = get_template('location/pull_manila_gps_websocket_data.py')
    rendered_tpl = template.render(context)
    pwd = getcwd()
    with TemporaryDirectory() as tempdir:
        file_name = join(tempdir, 'script.py')
        with open(file_name, 'x', encoding='utf-8') as f:
            f.write(rendered_tpl)
        cmd_txt = f'{environ["HOME"]}/.virtualenvs/data_management/bin/python {pwd}/manage.py shell < {file_name}'
        cmd = run(cmd_txt, capture_output=True, shell=True, text=True)
        WebsocketListener.objects.get(id=data.id).delete()
        return {
            'OUT': cmd.stdout,
            'ERR': cmd.stderr,
            'EQUIPMENT': data.__str__(),
            'ID': data.id
        }

