from bot.contents import stop, other, product, basket
from protocol.api.group import send_message
from json import loads

def text_parse(text: str):
    return text.split(' ')

def payload_parse(body_message: dict):
    if body_message.get('payload') is None:
        return {}
    return loads(body_message['payload'])

def handle(system, action_type, message, client_info):
        if system['stop'] is True:
            pass

        if action_type == 'message_new':
            if len(payload_parse(message)) > 0:
                args = payload_parse(message)
                if args.get('command') is not None:
                    args = text_parse(args.get('command'))
                    command = '/' + args[0]
                elif args.get('button') is not None:
                    args = text_parse(args.get('button'))
                    command = '/' + args[0]
                elif args.get('api') is not None:
                    handle_api(system, action_type, message, client_info)
                    return None
            else:
                args = text_parse(message['text'])
                command = args[0]

            if client_info.get('keyboard') is not True or client_info.get('carousel') is not True:
                send_message(message['peer_id'], 'Пожалуйста обновите приложение ВКонтакте, \n'
                                                 'в Вашей версии отсутствуют Кнопки или Карусель')
                return None

            if command == '/stop':
                stop.handle(system, message, client_info, args)

            if command == '/test':
                other.test(system, message, client_info, args)

            if command == '/start':
                other.start(system, message, client_info, args)

            if command == '/products':
                product.product_handler(system, message, client_info, args)

        pass

def handle_api(system, action_type, message, client_info):
    if action_type == 'message_new':
        if len(payload_parse(message)) > 0:
            args = payload_parse(message)
            if args.get('api') is not None:
                args = text_parse(args.get('api'))
                command = '/' + args[0]
        else:
            return None

        if client_info.get('keyboard') is not True or client_info.get('carousel') is not True:
            send_message(message['peer_id'], 'Пожалуйста обновите приложение ВКонтакте, \n'
                                             'в Вашей версии отсутствуют Кнопки или Карусель')
            return None

        if command == '/cart':
            basket.basket_handler(system, message, client_info, args)

    pass