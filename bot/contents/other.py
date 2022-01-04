from protocol.api import group

def start(system, body_message, client_info, args):
    group.send_message_keyboard(
        body_message['peer_id'],
        'Привет! Я ShopBot!\nПомогу тебе с выбором товара и его покупкой\n\n Нажми на кнопку "Посмотреть товары"',
        {
            'inline': False,
            'buttons': [
                [{
                    'action': {
                        'type': 'text',
                        'label': 'Посмотреть Товары',
                        'payload': '{"command": "products"}'
                    },

                    'color': 'primary',
            }]
        ]
    })
    pass