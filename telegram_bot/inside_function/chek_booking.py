import requests
import datetime
import json
from inside_function.config import load_config
from requests.exceptions import HTTPError
from pathlib import Path


def data_conversion(data_corp):
    rename_corp = {
        160000: 'Корпус 1. Общая кухня',
        161000: 'Корпус 2. Личная кухня',
        162000: 'Аппартаменты',
        163000: 'Коттедж',
    }
    name_list = list()
    message_text = str()
    for key in data_corp:
        message_text += rename_corp[key] + ':\t'
        message_text += str(data_corp[key]['plans_price']) + '\n'
        name_list.append(rename_corp[key])
        data_corp[key]['name'] = rename_corp[key]
    print(name_list)
    print(message_text)
    return message_text, name_list, data_corp


def chek_room(d_in, d_out, count):
    try:
        d_in = datetime.datetime.strftime(d_in, '%d-%m-%Y')
        d_out = datetime.datetime.strftime(d_out, '%d-%m-%Y')
        res = requests.get("ссылка на сайт с бронированием",
                           params={'account_id': 0000,
                                   'dfrom': d_in,
                                   'dto': d_out}
                           )
        data = res.json()
        dict_corp = dict()
        for key in data['rooms']:
            if key['adults'] >= count:
                dict_data = {
                    'count_guests': key['adults'],
                    'available': key['available'],
                    'plans_id': key['plans'][0]['id'],
                    'plans_prices': key['plans'][0]['prices'],
                    'plans_price': key['plans'][0]['price']
                }
                dict_corp[key['id']] = dict_data
            elif key['subrooms'][0]['adults'] == count:
                subroom = key['subrooms'][0]
                dict_data = {
                    'count_guests': subroom['adults'],
                    'available': key['available'],
                    'plans_id': subroom['plans'][0]['id'],
                    'plans_prices': subroom['plans'][0]['prices'],
                    'plans_price': subroom['plans'][0]['price']
                }
                dict_corp[subroom['id']] = dict_data
            else:
                continue
        for key in dict_corp:
            print(key)
            for key_2 in dict_corp[key]:
                print(key_2, '\t:\t', dict_corp[key][key_2])
        return data_conversion(dict_corp)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except KeyError as ky:
        print(f'Other error occurred: {ky}')
    except Exception as err:
        print(f'Other error occurred: {err}')


def get_token():
    config = load_config(flag=2)
    try:

        data_to_get = {
            "username": config.username,
            "password": config.password
        }
        res = requests.post("ссылка на API", json=data_to_get)
        data = res.json()
        token = data['token']
        return [1, token]
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return [0, 0]
    except Exception as err:
        print(f'Other error occurred: {err}')
        return [0, 0]


def post_data(data):
    try:
        res = requests.post("ссылка на API", json=data)
        answer = res.json()
        return True
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return False
    except Exception as err:
        print(f'Other error occurred: {err}')
        return False


def data_to_send(message, dict_data):
    input_server = dict_data['input_data']
    date_in = datetime.datetime.strftime(dict_data['date_in'], '%Y-%m-%d')
    date_out = datetime.datetime.strftime(dict_data['date_out'], '%Y-%m-%d')
    for key in input_server:
        if message.text == input_server[key]['name']:
            in_put = get_token()
            if in_put[0]:
                id_corp = key
                data_out = {
                    'token': in_put[1],
                    'account_id': 0000,
                    'booking_json': None}
                data_booking = {
                        'plan_id': input_server[id_corp]['plans_id'],
                        'warranty_type': 'no',
                        'arrival': date_in,
                        'departure': date_out,
                        'name': message['chat']['first_name'],
                        'surname': message.chat.username,
                        'email': 'test_email@gmail.com',
                        'phone': '+79999999999',
                        'lang': 'ru',
                        'room_types': {
                            id_corp: {
                                'count': 1,
                                'prices': input_server[id_corp]['plans_prices'],
                                'room_type_services': [
                                    {'services': []}
                                ],
                                    }
                        }
                    }
                data_out['booking_json'] = json.dumps(data_booking, ensure_ascii=False)
                file_name = (str(message['date'].strftime('%d_%m_%Y_%H_%M_%S'))
                             + '_' + str(message.chat.username)) + '.json'
                if post_data(data_out):
                    path = Path(Path.cwd(), 'log_booking', file_name)
                    with open(path, "w", encoding="utf8") as file:
                        json.dump(data_out, file, ensure_ascii=False)
                    return True
                else:
                    file_name = 'ERROR_server_' + file_name
                    path = Path(Path.cwd(), 'log_booking', file_name)
                    with open(path, "w", encoding="utf8") as file:
                        json.dump(data_out, file, ensure_ascii=False)
                    return False
            else:
                print('Ошибка получения токена')
                id_corp = key
                data_out = {
                    'token': 'ERROR',
                    'account_id': 0000,
                    'booking_json': {
                        'plan_id': input_server[id_corp]['plans_id'],
                        'warranty_type': 'no',
                        'arrival': date_in,
                        'departure': date_out,
                        'name': message['chat']['first_name'],
                        'surname': message.chat.username,
                        'email': 'test_email@gmail.com',
                        'phone': '+79999999999',
                        'lang': 'ru',
                        'room_types': {
                            id_corp: {
                                'count': 1,
                                'prices': input_server[id_corp]['plans_prices'],
                                'room_type_services': [],
                            }
                        }
                    }}

                file_name = str(message['date'].strftime('%d_%m_%Y_%H_%M_%S')
                                + '_' + str(message.chat.username) + '.json')
                file_name = 'ERROR_token_' + file_name
                path = Path(Path.cwd(), 'log_booking', file_name)
                with open(path, "w", encoding="utf16") as file:
                    json.dump(data_out, file, ensure_ascii=False)
                return False
        else:
            continue
    return False


def false_price(d_in, d_out):
    d_in = datetime.datetime.strftime(d_in, '%Y-%m-%d')
    d_out = datetime.datetime.strftime(d_out, '%Y-%m-%d')
    token = get_token()
    res = requests.get("ссылка на APi",
                params={'token': token[1],
                        'account_id': 0000,
                        'dfrom': d_in,
                        'dto': d_out,
                        'plans[]': 0000,
                        'fields[]':'price'}
                       )
    data = res.json()
    dict_price = {}
    for key in data['plans_data']['75951']:
        summ = 0
        for day in data['plans_data']['75951'][key]:
            summ += float(data['plans_data']['75951'][key][day]['price'])
        dict_price[key] = summ

    rename_corp = {
        160000: 'Корпус 1. Общая кухня',
        161000: 'Корпус 2. Личная кухня',
        162000: 'Аппартаменты',
        163000: 'Коттедж',
    }
    list_button = []
    text = str()
    for key in dict_price:
        text += rename_corp[int(key)] + '\t:\t' + str(dict_price[key]) + '\n\n'
        list_button.append(rename_corp[int(key)])
    return list_button, text



