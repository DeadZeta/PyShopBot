from protocol.api import group
import database.handler as database

def basket_handler(system, body_message, client_info, args):
    if len(args) >= 2:
        if args[1] == 'create':
            create_basket(system, body_message, client_info, args)
            return None

        if args[1] == 'checkout':
            checkout_basket(system, body_message, client_info, args)
            return None

        if args[1] == 'remove':
            remove_basket(system, body_message, client_info, args)
            return None

        if args[1] == 'edit':
            edit_basket_start(system, body_message, client_info, args)
            return None

def edit_basket_start(system, body_message, client_info, args):
    if len(args) >= 4:

        if args[2] == 'confirm':
            basket = database.get_basket(int(args[3]))

            if type(basket) is not tuple:
                group.send_message_keyboard(
                    body_message['peer_id'],
                    'Товара нет в корзине!'
                )

                return None

            if basket[1] == int(body_message['from_id']):
                group.send_message_keyboard(
                    body_message['peer_id'],
                    'Успешно отредактировано!'
                )

                checkout_basket(system, body_message, client_info, args)

                return None


        if args[2] == 'count_remove':
            basket = database.get_basket(int(args[4]))
            product = database.get_product(basket[2])
            new_count = int(args[3])

            if type(basket) is not tuple:
                group.send_message_keyboard(
                    body_message['peer_id'],
                    'Товара нет в корзине!'
                )

                return None

            if basket[1] == int(body_message['from_id']):
                count = basket[3] - new_count

                if count < product[4]:
                    group.send_message(
                        body_message['peer_id'],
                        f'Невозможно уменьшить товар!\nМинимальное количество товара - {str(product[4])}шт'
                    )

                    return None

                total_amount = product[3] * count
                database.update_basket(basket[0], 'count', count)
                database.update_basket(basket[0], 'total_amount', total_amount)

                group.send_message(
                    body_message['peer_id'],
                    f'Текущее количество - {str(count)}шт',
                )

        if args[2] == 'count_add':
            basket = database.get_basket(int(args[4]))
            product = database.get_product(basket[2])
            new_count = int(args[3])

            if type(basket) is not tuple:
                group.send_message_keyboard(
                    body_message['peer_id'],
                    'Товара нет в корзине!'
                )

                return None

            if basket[1] == int(body_message['from_id']):
                count = basket[3] + new_count

                if count > product[5]:
                    group.send_message(
                        body_message['peer_id'],
                        f'Невозможно увеличить товар!\nМаксимальное количество товара - {str(product[5])}шт'
                    )

                    return None

                total_amount = product[3] * count
                database.update_basket(basket[0], 'count', count)
                database.update_basket(basket[0], 'total_amount', total_amount)

                group.send_message(
                    body_message['peer_id'],
                    f'Текущее количество - {str(count)}шт',
                )

        if args[2] == 'count':
            basket = database.get_basket(int(args[3]))

            if type(basket) is not tuple:
                group.send_message_keyboard(
                    body_message['peer_id'],
                    'Товара нет в корзине!'
                )

                return None

            if basket[1] == int(body_message['from_id']):
                edit = {
                    'one_time': False,
                    'buttons': [
                        [
                            {
                                'action': {
                                    'type': 'text',
                                    'label': '-10',
                                    'payload': '{"api": "cart edit count_remove 10 '
                                               '' + str(basket[0]) + '"}'
                                }
                            },
                            {
                                'action': {
                                    'type': 'text',
                                    'label': '-1',
                                    'payload': '{"api": "cart edit count_remove 1 '
                                               '' + str(basket[0]) + '"}'
                                }
                            },
                            {
                                'action': {
                                    'type': 'text',
                                    'label': 'Y',
                                    'payload': '{"api": "cart edit confirm '
                                               '' + str(basket[0]) + '"}'
                                }
                            },
                            {
                                'action': {
                                    'type': 'text',
                                    'label': '+1',
                                    'payload': '{"api": "cart edit count_add 1 '
                                               '' + str(basket[0]) + '"}'
                                }
                            },
                            {
                                'action': {
                                    'type': 'text',
                                    'label': '+10',
                                    'payload': '{"api": "cart edit count_add 10 '
                                               '' + str(basket[0]) + '"}'
                                }
                            }
                        ]
                    ]
                }

                group.send_message_keyboard(
                    body_message['peer_id'],
                    f'Текущее количество - {basket[3]}шт',
                    edit
                )

def remove_basket(system, body_message, client_info, args):
    if len(args) == 3:
        basket = database.get_basket(int(args[2]))

        if type(basket) is not tuple:
            group.send_message_keyboard(
                body_message['peer_id'],
                'Товара нет в корзине!'
            )

            return None

        if basket[1] == int(body_message['from_id']):
            database.remove_basket(basket[0])

            group.send_message(
                body_message['peer_id'],
                'Товар успешно удален из корзины!'
            )

            args = ['cart', 'checkout']

            checkout_basket(system, body_message, client_info, args)

def checkout_basket(system, body_message, client_info, args):
    baskets = []
    baskets_id = []
    all_total_amount = 0

    for basket in database.get_actived_baskets_on_user(int(body_message['from_id'])):
        baskets_id.append(basket[0])

    if len(baskets_id) <= 0:
        group.send_message_keyboard(
            body_message['peer_id'],
            'У Вас нету товаров в корзине!'
        )
        return None

    for basket in baskets_id:
        basket = database.get_basket(basket)
        product = database.get_product(basket[2])

        if type(product) is not tuple:
            database.update_basket(basket[0], 'status', 'cancel')
            continue

        all_total_amount += int(basket[4])

        baskets.append({
            'title': product[1],
            'description': 'Количество: ' + str(basket[3]) + 'шт',
            'photo_id': '-109837093_457242809',
            'buttons': [
                {
                    'action': {
                        'type': 'text',
                        'label': 'Изменить количество',
                        'payload': '{"api": "cart edit count ' + str(basket[0]) + '"}'
                    }
                },
                {
                    'action': {
                        'type': 'text',
                        'label': 'Удалить товар',
                        'payload': '{"api": "cart remove ' + str(basket[0]) + '"}'
                    }
                }
            ]
        })

    payment = {
        'one_time': False,
        'buttons': [
            [
                {
                    'action': {
                        'type': 'text',
                        'label': 'Оплатить',
                        'payload': '{"api": "kassa preview"}'
                    }
                }
            ]
        ]
    }

    group.send_message_carousel(
        body_message['peer_id'],
        f'Общая стоимость (в рублях) - {all_total_amount}\n\nСписок товаров в Вашей корзине:',
        {
            'type': 'carousel',
            'elements': baskets,
        }
    )

    group.send_message_keyboard(
        body_message['peer_id'],
        'Для оформления оплаты перейдите по Кнопке...',
        payment
    )

def create_basket(system, body_message, client_info, args):
    if len(args) == 5:
        mode = args[2]
        product_id = int(args[3])
        product = database.get_product(product_id)

        count_basket = database.count_actived_baskets_on_user(body_message['from_id'])

        if len(count_basket) == 10:
            group.send_message(body_message['peer_id'], 'Сожалеем, но Ваша корзина переполнена.')
            return None

        if type(product) is not tuple:
            group.send_message(body_message['peer_id'], 'Извините, но товар снят с продажи...')
            return None

        count = int(args[4])
        total_amount = product[3] * count
        buyer = int(body_message['from_id'])
        already_exists = [False, ()]

        for basket in database.get_actived_baskets_on_user(int(body_message['from_id'])):
            if basket[2] == product_id:
                already_exists = [True, basket]
                break

        if already_exists[0]:
            new_count = already_exists[1][3] + count
            new_total = already_exists[1][3] * product[3]

            database.update_basket(already_exists[1][0], 'count', new_count)
            database.update_basket(already_exists[1][0], 'total_amount', new_total)
        else:
            database.create_basket({
                'buyer': buyer,
                'product': product_id,
                'count': count,
                'total_amount': total_amount,
                'status': 'active'
            })

        if mode == 'no_skip':
            args = ['cart', 'checkout']
            checkout_basket(system, body_message, client_info, args)
        elif mode == 'skip_checkout':
            group.send_message_keyboard(
                body_message['peer_id'],
                'Отлично! Ваш товар добавлен в корзину',
                {
                    'inline': True,
                    'buttons': [
                        [
                            {
                                'action': {
                                    'type': 'text',
                                    'label': 'Перейти к оформлению',
                                    'payload': '{"api": "cart checkout"}'
                                }
                            }
                        ]
                    ]
                }
            )
    pass