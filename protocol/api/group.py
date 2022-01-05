from protocol.api.base import user_send_api, group_send_api, rand
from time import time as unixtime
from json import dumps

def send_message(peer_id: int, message: str):
    return group_send_api('messages.send', {
        'peer_id': peer_id,
        'message': message,
        'random_id': rand()
    })

def send_message_keyboard(peer_id: int, message: str,
                          keyboard: dict = {'one_time': False, 'buttons': []}):
    return group_send_api('messages.send', {
        'peer_id': peer_id,
        'message': message,
        'keyboard': dumps(keyboard),
        'random_id': rand()
    })

def send_message_carousel(peer_id: int, message: str,
                          carousel: dict = {}):
    return group_send_api('messages.send', {
        'peer_id': peer_id,
        'message': message,
        'template': dumps(carousel),
        'random_id': rand()
    })

def send_message_multi(peer_id: int, message: str,
                          carousel: dict = {}, keyboard: dict = {'one_time': True, 'buttons': []}):
    return group_send_api('messages.send', {
        'peer_id': peer_id,
        'message': message,
        'template': dumps(carousel),
        'keyboard': dumps(keyboard),
        'random_id': rand()
    })

def wall_post(owner_id: int, message: str,
              comments: bool = True, publish_date: int = 0):
    return user_send_api('wall.post', {
        'owner_id': -owner_id,
        'message': message,
        'from_group': 1,
        'close_comments': 1 if comments else 0,
        'publish_date': int(unixtime()) + publish_date if publish_date != 0 else publish_date
    })
