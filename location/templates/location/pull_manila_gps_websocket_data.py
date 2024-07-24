from asyncio import run
from datetime import datetime
from django.conf import settings
from django.contrib.gis.geos import Point
from django.utils.dateparse import parse_datetime as pdt
from json import dumps, loads
from websockets import connect
from zoneinfo import ZoneInfo

from custom.models import Log
from location.models.equipment import ManilaGpsWebsocketData

equipment = '{{ EQUIPMENT }}'
id = {{ ID }}
hash_value = '{{ HASH }}'
tracker_id = {{ TRACKER_ID }}

json_send = {
    'action': 'subscribe',
    'hash': hash_value,
    'events': ['state'],
    'trackers': [tracker_id]
}

async def process_data(data):
    if 'action' in data:
        if 'state' in data['data']:
            mgps = await ManilaGpsWebsocketData.objects.aget(id=id)
            mgps.call_time = datetime.now(ZoneInfo(settings.TIME_ZONE))
            if data['data']['state']['value'][str(tracker_id)] == 'blocked':
                if mgps.last_blocked is None or mgps.last_success >  mgps.last_blocked:
                    mgps.last_blocked = mgps.call_time
            elif data['data']['state']['value'][str(tracker_id)] == 'normal':
                mgps.last_success = mgps.call_time
            else:
                await Log(log=f'Unknown state.\nEquipment: {equipment}\n{dumps(data)}').asave()
            await mgps.asave()
        else:
            await Log(log=f'Unknown event subscription.\nEquipment: {equipment}\n{dumps(data)}').asave()
    elif 'data' in data and 'source_id' in data['data']:
        mgps = await ManilaGpsWebsocketData.objects.aget(id=id)
        mgps.alt = data['data']['gps']['alt']
        mgps.battery_level = data['data']['battery_level']
        mgps.connection_status = data['data']['connection_status']
        mgps.geom = Point(x=data['data']['gps']['location']['lng'], y=data['data']['gps']['location']['lat'], srid=4326)
        mgps.heading = data['data']['gps']['heading']
        mgps.lat = data['data']['gps']['location']['lat']
        mgps.lon = data['data']['gps']['location']['lng']
        mgps.movement_status = data['data']['movement_status']
        mgps.network_name = data['data']['gsm']['network_name']
        mgps.signal_level = data['data']['gsm']['signal_level']
        mgps.speed = data['data']['gps']['speed']
        mgps.update_battery = pdt(f'{data["data"]["battery_update"]}+0800')
        mgps.update_gps = pdt(f'{data["data"]["gps"]["updated"]}+0800')
        mgps.update_gsm = pdt(f'{data["data"]["gsm"]["updated"]}+0800')
        mgps.update_last = pdt(f'{data["data"]["last_update"]}+0800')
        await mgps.asave()
    else:
        await Log(log=f'Unknown JSON response.\nEquipment: {equipment}\n{dumps(data)}').asave()

async def on_message(ws, message):
    if "X" in message:
        await ws.close()
    else:
        await process_data(loads(message))

async def listen(ws):
    async for message in ws:
        await on_message(ws, message)

async def ws_connect():
    uri = 'wss://api.gpstrack.global/event/subscription?X-Atmosphere-tracking-id=0&Content-Type=application/json&X-atmo-protocol=true'
    async with connect(uri) as ws:
        await ws.send(dumps(json_send))
        await ws.close()
        await listen(ws)

async def main():
    await ws_connect()

run(main())

