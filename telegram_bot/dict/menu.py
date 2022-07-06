from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from inside_function.text_read import read_text
import inside_function.logic_bot as lg
import inside_function.tele_logic as tl
import inside_function.config as conf


config = conf.load_config(flag=1)

class Step(StatesGroup):
    step_0 = State()
    step_1 = State()


class Def(StatesGroup):
    about_us = State()
    entertainments = State()
    booking = State()
    admin_mode = State()


async def start_bot(message: types.Message):
    """
    Bot logic for the start command
    Creates buttons for the main menu
    :param message: aiogram.message
    :return:
    """
    print(message)
    print(message.text)
    await lg.log_bot(message)
    if str(message.chat.id) in config.admin_id:
        await message.answer(read_text('other.txt', position=0),
                             reply_markup=tl.create_button(key='main_menu_1'))
        await Step.step_1.set()
    else:
        await message.answer(read_text('other.txt', position=0),
                             reply_markup=tl.create_button(key='main_menu_0'))
        await Step.step_1.set()


async def main_menu(message: types.Message, state: FSMContext):
    """
    Bot logic for the main menu(alternative start command)
    Creates buttons for the main menu
    :param message:
    :param state:
    :return:
    """
    print(message)
    print(message.text)
    if str(message.chat.id) in config.admin_id:
        await message.answer(read_text('other.txt', position=1),
                             reply_markup=tl.create_button(key='main_menu_1'))
        await Step.step_1.set()
    else:
        await message.answer(read_text('other.txt', position=1),
                             reply_markup=tl.create_button(key='main_menu_0'))
        await Step.step_1.set()


async def menu_start(message: types.Message, state: FSMContext):
    """
    Logic bot
    Creates buttons for level 2 sections.
    :param message:
    :param state:
    :return:
    """
    print(message)
    print(message.text)
    await lg.log_bot(message)

    if message.text == tl.name_button['main_menu_1'][0]:
        await message.answer(read_text('int_answer_cat.txt', intr=True),
                             reply_markup=tl.create_button(key='about_us_0'))
        await Def.about_us.set()

    elif message.text == tl.name_button['main_menu_1'][1]:
        await message.answer(read_text('int_answer_cat.txt', intr=True),
                             reply_markup=tl.create_button(key='about_e'))
        await Def.entertainments.set()

    elif message.text == tl.name_button['main_menu_1'][2]:
        config = conf.load_config(flag=1)
        # все ссылки заменены
        url_s = f'telegram.me/{config.admin_name[config.active_admin]}'
        url_cite = 'https://www.pass'
        url_vk = 'https://vk.com/pass'
        url_feedback = 'https://yandex.ru/maps/org/pass'
        buttons = [
                types.InlineKeyboardButton(text='Менеджер', url=url_s),
                types.InlineKeyboardButton(text='Мы в VK', url=url_vk),
                types.InlineKeyboardButton(text='Наш сайт', url=url_cite),
                types.InlineKeyboardButton(text='Отзывы о нас', url=url_feedback)
                   ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        await message.answer(read_text('other.txt', position=2), reply_markup=keyboard)
        return

    elif message.text == tl.name_button['main_menu_1'][3]:
        await message.answer(read_text('int_answer_cat.txt', intr=True),
                             reply_markup=tl.create_button(key='booking_0'))
        await Def.booking.set()

    elif message.text == tl.name_button['main_menu_1'][4]:
        await message.answer(read_text('int_answer_cat.txt', intr=True),
                             reply_markup=tl.create_button(key='admin_panel'))
        await Def.admin_mode.set()

    else:
        await message.answer(read_text('int_not_button.txt', intr=True))
        return


async def disclamer(message: types.Message, state: FSMContext):
    """
    Logic bot for unexpected text messages
    :param message:
    :param state:
    :return:
    """
    print(message)
    print(message.text)
    with open('text.txt', 'w', newline='', encoding='utf8') as fl:
        fl.write(message.text)
        fl.close()
    await lg.log_bot(message)
    url_s = f'telegram.me/{config.admin_name[config.active_admin]}'
    buttons = [types.InlineKeyboardButton(text='Менеджер', url=url_s)]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer(read_text('int_not_command.txt', intr=True), reply_markup=keyboard)


# вспомогательная функция для отладки
async def read_photo(message: types.Message):
    print(message)
    print(message.photo[-1].file_id)
    with open('photo.txt', 'a', newline='') as fl:
        text = message.photo[-1].file_id + '\n'
        fl.write(text)
        fl.close()




def register_handlers_main_menu(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands='start', state='*')
    dp.register_message_handler(main_menu, state=Step.step_0)
    dp.register_message_handler(menu_start, state=Step.step_1)
    dp.register_message_handler(disclamer, content_types=types.ContentType.TEXT, state=None)
    dp.register_message_handler(read_photo, content_types=types.ContentType.PHOTO, state=None)
    dp.register_message_handler(read_photo, content_types=types.ContentType.DOCUMENT, state=None)
