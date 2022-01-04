import requests
from json import loads, dumps
import config
from random import randint

VK_API_URL = "https://api.vk.com/method/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}

def group_send_api(method: str, params: dict):
    params['access_token'] = config.group_token,
    params['v'] = config.version,

    response = requests.post(VK_API_URL + method, data = params, headers=headers)

    if response.status_code != 200:
        print("Error: status code is not 200")
        exit()

    if loads(response.text).get('error') is not None:
        print("Error:", loads(response.text).get('error')['error_msg'])
        exit()

    return loads(response.text)

def user_send_api(method: str, params: dict):
    params['access_token'] = config.user_token,
    params['v'] = config.version,

    response = requests.post(VK_API_URL + method, data = params, headers=headers, timeout=3)

    if response.status_code != 200:
        print("Error: status code is not 200")
        exit()

    if loads(response.text).get('error') is not None:
        print("Error:", loads(response.text).get('error')['error_msg'])
        exit()

    return loads(response.text)

def send_server(system, longpoll: dict):
    act = 'a_check',
    wait = 3

    try:
        response = requests.get(longpoll['server'],
                            params={'act': act, 'wait': wait, 'key': longpoll['key'], 'ts': longpoll['ts']},
                            headers=headers,
                            timeout=3)
    except requests.exceptions.ReadTimeout:
        system['reconnect'] = True

        return {}

    if response.status_code != 200:
        print("Error: status code is not 200")
        exit()

    if response.text == '' or None:
        print("Warning: Server return Empty text")
        return {}

    if loads(response.text).get('failed') is not None:
        if loads(response.text).get('failed') != 1:
            system['reconnect'] = True

            return {}
        else:
            system['connect_back'] = True
            longpoll['ts'] = loads(response.text).get('ts')

            return {}

    return loads(response.text)

def rand():
    return randint(0, 99999999999999)