from pathlib import Path
from aiogram import types
import random


def read_text(name: str, intr=False, position=-1):
    """
    Функция принимает имя файла и два флага,
    открывает указанный файл, по флагам возвращает:
    или список текса, или случайный текст
    или конкретный текст из файла
    :param name: str, название файла
    :param intr: bool, вернуть ли случайный текст
    :param position: int, вернуть ли конкретный текст
    :return: text[list or str]
    """
    try:
        path = Path(Path.cwd(), 'text', name)
        with open(path, 'rt', encoding='utf-8') as file:
            text_file = file.read()
            file.close()
    except:
        return 'Ошибка, файл не найден!'
    if not intr and position != -1:
        text = text_file.split('==\n')
        return text[position]
    elif intr and position == -1:
        text = text_file.split('==\n')
        return random.choice(text)
    elif not intr and position == -1:
        text = text_file.split('==\n')
        return text
    else:
        return 'Ошибка, обратитесь к менеджеру'


def read_photo(name_file: str):
    try:
        path = Path(Path.cwd(), 'photo', name_file)
        with open(path, 'rt', encoding='utf-8') as file:
            text_file = file.read()
            file.close()
    except:
        return 'Ошибка, файл не найден!'
    text_file = text_file.split('\n')
    photo_id = list()
    for file_id in text_file:
        photo_id.append(types.input_media.InputMediaPhoto(file_id))
    return photo_id


def list_text():
    path = Path(Path.cwd(), 'text').rglob("*.txt")
    list_f = []
    for file in path:
        file = file.name
        list_f.append(file)
    return list_f


def list_photo():
    path = Path(Path.cwd(), 'photo').rglob("*.txt")
    list_f = []
    for file in path:
        file = file.name
        list_f.append(file)
    return list_f

