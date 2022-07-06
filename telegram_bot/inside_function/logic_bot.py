import datetime
import pandas as pd
from pathlib import Path
import csv

path = Path(Path.cwd(), 'log_bot.csv')


async def log_bot(message):
    """
    This function collects user data
    and stores it in the log file "log_bot.csv"
    :param message: telegram message class
    :return: None
    """
    data = dict()
    print(message)
    data['message_id'] = message['message_id']
    list_data = ['id', 'first_name', 'last_name', 'username', 'type']
    for key in list_data:
        try:
            data[key] = message['chat'][key]
        except:
            data[key] = ''
    data['date_message'] = message['date'].strftime('%d-%m-%Y %H:%M:%S')
    data['text'] = message['text']
    with open('log_bot.csv', 'a', encoding='utf16') as file:
        wr = csv.DictWriter(file, fieldnames=data.keys(), delimiter=';')
        wr.writerow(data)


def static_data():
    """
    Retrieves data about unique users from the logfile
    :return: str - unique users and count messages
    """
    df = pd.read_csv(path, sep=';', encoding='utf16')
    user = df['username'].value_counts()
    line = df.shape[0]
    username = str()
    user = user.to_dict()
    count = len(user)
    for name in user:
        username += str(name) + ' : ' + str(user[name]) + '\n'
    usernames = f'Всего пользователей писало боту: {count}\n' + f'Бот получил всего сообщений: {line}\n' + username
    return usernames


def all_user():
    """
    Creates list unique users.
    :return: list
    """
    df = pd.read_csv(path, sep=';', encoding='utf16')
    chat_unique = df['id'].unique()
    print(chat_unique)
    return chat_unique


def this_date(text):
    """
    Logic bot.
    Checks whether the data is filled in correctly.
    :param text:
    :return:
    """
    text = text.split('-')
    try:
        date_in = datetime.datetime.strptime(text[0].strip(), '%d.%m.%Y').date()
        date_out = datetime.datetime.strptime(text[1].strip(), '%d.%m.%Y').date()
    except:
        return [0, 'Неверный формат даты. Повторите ввод дат.']
    date_now = datetime.date.today()
    if date_in > date_out:
        return [0, 'Ошибка! Дата заезда позже даты выезда. Повторите ввод дат.']
    if date_in < date_now:
        return [0, 'Ошибка! Дата заезда позже сегодняшней даты!']
    return [1, date_in, date_out]



