from protocol.api import group

def handle(system, body_message, client_info, args):
    group.send_message(body_message['peer_id'], 'Завершение работы...')
    system['stop'] = True

    pass