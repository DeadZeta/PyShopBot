from protocol.api.base import user_send_api, rand
from time import time as unixtime

def send_message(user_id: int, message: str):
    return user_send_api('messages.send', {
        'user_id': user_id,
        'message': message,
        'random_id': rand()
    })

def wall_get(owner_id: int, count: int = 1, offset: int = 0):
    return user_send_api('wall.get', {
        'owner_id': owner_id,
        'offset': offset,
        'count': count
    })

def wall_post(group_id: int, message: str,
              comments: bool = True, publish_date: int = 0):
    return user_send_api('wall.post', {
        'owner_id': -group_id,
        'message': message,
        'close_comments': 1 if comments else 0,
        'publish_date': int(unixtime()) + publish_date if publish_date != 0 else publish_date
    })
