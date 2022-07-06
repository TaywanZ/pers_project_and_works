from aiogram import types


name_button = {
    'main_menu_0': ['☀️О нас', '🎡Развлечения', '📲Контакты', '🔑Бронирование'],
    'main_menu_1': ['☀️О нас', '🎡Развлечения', '📲Контакты', '🔑Бронирование', 'Админ панель'],
    'about_us_0': ['👨‍👩‍👧‍👦Кто мы', '🚘Как добраться', '🏘Номера', '🏞Территория', '🗺О посёлке', '🌤Погода', 'Назад'],
    'about_us_1': ['🚖Транспортные узлы', 'Наш адрес', 'Назад'],
    'about_us_2': ['Корпус 1', 'Корпус 1 с кухней', 'Корпус 2 с кухней', 'Аппартаменты', 'Коттедж', 'Назад', '🔑Забронировать'],
    'about_us_3': ['Информация о посёлке', 'Что есть в посёлке', 'Назад'],
    'about_e': ['🧉Вечеринки', '🎉Анимация', '🏔Экскурсии', '🎢Аттракционы', 'Назад'],
    'booking_0': ['Найти свободные номера', 'Отмена'],
    'booking_1': ['🔑Забронировать', 'Отмена'],
    'feedback': ['🗣Написать отзыв', 'Прочитать отзыв', 'Назад'],
    'admin_panel': ['🗣Массовая рассылка', 'Статистика бота', 'Правка файлов', 'Правка фото', 'Активный админ', 'Назад'],
}


def create_button(key=None, list_button=None):
    """
    This function creates buttons from the dict "name_button"
    :param key: key from the dict "name_button"
    :param list_button: list with the names of the buttons
    :return: object, aiogram buttons
    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if not list_button:
        buttons_list = name_button[key]
        for i in range(0, len(buttons_list), 2):
            keyboard.add(*(buttons_list[i: i + 2]))
        return keyboard
    else:
        for i in range(0, len(list_button), 2):
            keyboard.add(*(list_button[i: i + 2]))
        return keyboard
