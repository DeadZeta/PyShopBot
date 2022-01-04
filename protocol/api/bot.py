from protocol.api.base import group_send_api

def get_server(group_id: int):
    return group_send_api('groups.getLongPollServer', {
        'group_id': group_id
    })