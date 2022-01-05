from protocol.api import group
import database.handler as database

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
        }
    )

    pass

def test(system, body_message, client_info, args):
    database.create_product({
        'name': '1',
        'description': 'test',
        'price': 10,
        'min_count': 1,
        'max_count': 10
    })

    database.create_product({
        'name': '2',
        'description': 'test2',
        'price': 20,
        'min_count': 1,
        'max_count': 10
    })

    database.create_product({
        'name': '3',
        'description': 'test3',
        'price': 30,
        'min_count': 1,
        'max_count': 10
    })

    database.create_product({
        'name': '4',
        'description': 'test4',
        'price': 40,
        'min_count': 1,
        'max_count': 10
    })

    database.create_product({
        'name': '5',
        'description': 'test5',
        'price': 50,
        'min_count': 1,
        'max_count': 10
    })

    database.create_product({
        'name': '6',
        'description': 'test6',
        'price': 60,
        'min_count': 1,
        'max_count': 10
    })

    database.create_product({
        'name': '7',
        'description': 'test7',
        'price': 70,
        'min_count': 1,
        'max_count': 10
    })

    database.create_product({
        'name': '8',
        'description': 'test8',
        'price': 80,
        'min_count': 1,
        'max_count': 10
    })

    database.create_product({
        'name': '9',
        'description': 'test9',
        'price': 90,
        'min_count': 1,
        'max_count': 10
    })

    database.create_product({
        'name': '10',
        'description': 'test10',
        'price': 100,
        'min_count': 1,
        'max_count': 10
    })

    database.create_product({
        'name': '11',
        'description': 'test11',
        'price': 110,
        'min_count': 1,
        'max_count': 10
    })

    database.create_product({
        'name': '12',
        'description': 'test12',
        'price': 120,
        'min_count': 1,
        'max_count': 10
    })

    database.create_product({
        'name': '13',
        'description': 'test13',
        'price': 130,
        'min_count': 1,
        'max_count': 10
    })

    database.create_product({
        'name': '14',
        'description': 'test14',
        'price': 140,
        'min_count': 1,
        'max_count': 10
    })

    database.create_product({
        'name': '15',
        'description': 'test15',
        'price': 150,
        'min_count': 1,
        'max_count': 10
    })

    group.send_message(
        body_message['peer_id'],
        'success',
    )

    pass