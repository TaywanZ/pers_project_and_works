import random
from pathlib import Path


def write_feedback(message, name_text=None):
    """
    Функция записи фидбэка пользователя в txt файл.
    :param message: Any
    :return: None
    """
    if not name_text:
        name_file = str(message['date'].strftime('%d_%m_%Y_%H_%M_%S') + '_' + message.chat.username)
        path = Path(Path.cwd(), 'feed_back', f'{name_file}.txt')
        text_feedback = message.text
        with open(path, 'a', encoding='utf8', newline='') as f_object:
            f_object.write(text_feedback)
            f_object.close()
        return name_file
    else:
        try:
            path = Path(Path.cwd(), 'text', name_text)
            text_feedback = message                         # передается только текст
            with open(path, 'w', encoding='utf8', newline='') as f_object:
                f_object.write(text_feedback)
                f_object.close()
            return True
        except:
            return False


def read_feedback(name_text=None):
    """
    Функция чтения случайного фидбэка из txt файла,
    путём прочтения списка файлов с фидбэками из файла
    main_file.txt и прочтения конечного файла.
    :return: тескт фидбэка
    """
    if not name_text:
        try:
            path = Path(Path.cwd(), 'feed_back').rglob("*.txt")
            list_f = list()
            for file in path:
                list_f.append(file.name)
            name_file = list_f[random.randint(0, len(list_f) - 1)]
            path_fb = Path(Path.cwd(), 'feed_back', name_file)
            with open(path_fb, 'rt', encoding='utf8', newline='') as f_object:
                text = f_object.read()
                f_object.close()
            return text
        except:
            return 'Ошибка, действие не выполнено'

    else:
        path = Path(Path.cwd(), 'text', name_text)
        with open(path, 'rt', encoding='utf8', newline='') as f_object:
            text = f_object.read()
            f_object.close()
        return text

