from protocol.api import group
import database.handler as database

diapason = 4

def builder(min, max):
    elements = []
    for product in database.range_products({'from': min, 'to': max}):
        count = 1

        elements.append({
            'title': product[1],
            'description': product[2],
            'photo_id': '-109837093_457242809',
            'buttons': [
                {
                    'action': {
                        'type': 'text',
                        'label': 'Добавить в корзину',
                        'payload': '{"api": "cart create skip_checkout '
                                   '' + str(product[0]) + ' ' + str(count) + '"}'
                    }
                },
                {
                    'action': {
                        'type': 'text',
                        'label': f'Купить за {product[3]} руб',
                        'payload': '{"api": "cart create no_skip '
                                   '' + str(product[0]) + ' 1"}'
                    }
                }
            ]
        })

    switcher = {
        'one_time': False,
        'buttons': []
    }

    if max + diapason <= database.last_id('product'):
        page = max + diapason + 1
        switcher['buttons'].append([
            {
                'action': {
                    'type': 'text',
                    'label': '<-',
                    'payload': '{"command": "products page previous ' + str(page) + '"}'
                }
            }
        ])

    if min - 1 > 0:
        page = min - 1
        switcher['buttons'].append([
                    {
                        'action': {
                            'type': 'text',
                            'label': '->',
                            'payload': '{"command": "products page next ' + str(page) + '"}'
                        }
                    }
                ])

    return [elements, switcher]

def product_handler(system, body_message, client_info, args):
    if len(args) == 1:
        start_products(system, body_message, client_info, args)
        return None

    if len(args) > 2:
        if args[1] == 'page':
            page_products(system, body_message, client_info, args)
            return None

def start_products(system, body_message, client_info, args):
    last_products = database.last_id('product')

    if last_products-diapason <= 0:
        min_products = 1
    else:
        min_products = last_products - diapason

    build = builder(min_products, last_products)

    group.send_message_carousel(
        body_message['peer_id'],
        'Вот список последних товаров',
        {
            'type': 'carousel',
            'elements': build[0],
        }
    )

    group.send_message_keyboard(
        body_message['peer_id'],
        'Для того что бы посмотреть больше товаров нажимай кнопки "<-" или "->"',
        build[1]
    )
    pass

def page_products(system, body_message, client_info, args):
    if len(args) == 4:
        if args[2] == 'next':
            max = int(args[3])

            if max - diapason <= 0:
                min = 1
            else:
                min = max - diapason

            build = builder(min, max)

        if args[2] == 'previous':
            max = int(args[3])

            if max - diapason <= 0:
                min = 1
            else:
                min = max - diapason

            build = builder(min, max)

        group.send_message_carousel(
            body_message['peer_id'],
            'Вот список последних товаров',
            {
                'type': 'carousel',
                'elements': build[0],
            }
        )

        group.send_message_keyboard(
            body_message['peer_id'],
            'Для того что бы посмотреть больше товаров нажимай кнопки "<-" или "->"',
            build[1]
        )