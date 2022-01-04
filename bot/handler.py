from bot.contents import stop, other
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
                    command = '/' + args.get('command')
                else:
                    command = '/' + args.get('button')
            else:
                args = text_parse(message['text'])
                command = args[0]

            if command == '/stop':
                stop.handle(system, message, client_info, args)

            if command == '/start':
                menu.handle(system, message, client_info, args)

        pass