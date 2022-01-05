from protocol.api import base, bot
import config
from bot.handler import handle
from database.handler import create_tables
from threading import Thread

longpoll = {
    'key': '',
    'server': '',
    'ts': 0
}

system = {
    'connect_back': False,
    'reconnect': False,
    'stop': False
}

def init():
    server = bot.get_server(config.group_id)

    longpoll['key'] = server['response'].get('key')
    longpoll['server'] = server['response'].get('server')
    longpoll['ts'] = int(server['response'].get('ts'))

    create_tables()

    listen()

def listen():
    while True:
        if system.get('reconnect') == True:
            server = bot.get_server(config.group_id)

            longpoll['key'] = server['response'].get('key')
            longpoll['server'] = server['response'].get('server')
            longpoll['ts'] = server['response'].get('ts')
            system['reconnect'] = False

        if system.get('connect_back') == True:
            server = bot.get_server(config.group_id)

            longpoll['key'] = server['response'].get('key')
            longpoll['server'] = server['response'].get('server')
            system['reconnect'] = False

        if system.get('stop') == True:
            system['stop'] = False
            exit()
            break

        server = base.send_server(system, longpoll)

        if server.get('updates') is None:
            continue

        if len(server.get('updates')) == 0:
            if longpoll['ts'] == server.get('ts'):
                continue

            longpoll['ts'] += 1
            continue

        thread = Thread(target=handle, args=(system, server.get('updates')[0]['type'],
                                     server.get('updates')[0]['object']['message'],
                                     server.get('updates')[0]['object']['client_info']))
        thread.start()

        longpoll['ts'] = int(longpoll['ts'])
        longpoll['ts'] += 1

        continue