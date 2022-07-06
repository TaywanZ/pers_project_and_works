from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from dict.menu import main_menu, Step, Def
from inside_function.weawer_responce import request_forecast
from inside_function.text_read import read_text, read_photo
import inside_function.logic_bot as lg
import inside_function.tele_logic as tl


class About(StatesGroup):
    about_way = State()
    about_room = State()
    about_village = State()


async def about_us_one_step(message: types.Message, state: FSMContext):
    """
    Logic bot.
    Creates buttons for level 3 section.
    :param message:
    :param state:
    :return:
    """
    print(message)
    print(message.text)
    await lg.log_bot(message)

    if message.text not in tl.name_button['about_us_0']:
        await message.answer(read_text('int_not_button.txt', intr=True))
        return

    elif message.text == tl.name_button['about_us_0'][0]:
        text_list = read_text('about_us.txt')
        await message.answer_media_group(media=read_photo('photo_us.txt'))
        for k in range(len(text_list)):
            await message.answer(text_list[k], parse_mode='Markdown')
        return

    elif message.text == tl.name_button['about_us_0'][1]:
        await message.answer(read_text('int_answer_cat.txt', intr=True),
                             reply_markup=tl.create_button(key='about_us_1'),
                             parse_mode='Markdown')
        await About.about_way.set()

    elif message.text == tl.name_button['about_us_0'][2]:
        text_list = read_text('about_room.txt')
        for k in range(len(text_list)-1):
            await message.answer(text_list[k], parse_mode='Markdown')
        await message.answer(text_list[-1],
                             reply_markup=types.ReplyKeyboardRemove(),
                             parse_mode='Markdown')
        await message.answer(read_text('other.txt', position=3),
                             reply_markup=tl.create_button(key='about_us_2'))
        await About.about_room.set()

    elif message.text == tl.name_button['about_us_0'][3]:
        text_list = read_text('about_area.txt')
        await message.answer_media_group(media=read_photo('photo_area.txt'))
        for k in range(len(text_list)):
            await message.answer(text_list[k], parse_mode='Markdown')
        return

    elif message.text == tl.name_button['about_us_0'][4]:
        text_list = read_text('about_village.txt')
        await message.answer_media_group(media=read_photo('photo_village.txt'))
        for k in range(len(text_list) - 1):
            await message.answer(text_list[k], parse_mode='Markdown')
        await message.answer(text_list[-1],
                             reply_markup=types.ReplyKeyboardRemove(),
                             parse_mode='Markdown')
        await message.answer(read_text('other.txt', position=9),
                             reply_markup=tl.create_button(key='about_us_3'))
        await About.about_village.set()
        return

    elif message.text == tl.name_button['about_us_0'][5]:
        await message.answer(request_forecast(), parse_mode='Markdown')
        return

    else:
        await message.answer(read_text('int_cancle.txt', intr=True))
        await Step.step_0.set()
        await main_menu(message, state)


async def about_us_two_step(message: types.Message, state: FSMContext):
    """
    Logic bot.
    Tells about the hotel rooms
    :param message:
    :param state:
    :return:
    """
    print(message)
    print(message.text)
    await lg.log_bot(message)
    if message.text not in tl.name_button['about_us_2']:
        await message.answer(read_text('int_not_button.txt', intr=True))
        return
    elif message.text == tl.name_button['about_us_2'][0]:
        text_list = read_text('about_corp_1.txt')
        for k in range(len(text_list)):
            await message.answer(text_list[k], parse_mode='Markdown')
        await message.answer_media_group(media=read_photo('photo_corp_1_common.txt'))
        return
    elif message.text == tl.name_button['about_us_2'][1]:
        text_list = read_text('about_corp_1_1.txt')
        for k in range(len(text_list)):
            await message.answer(text_list[k], parse_mode='Markdown')
        await message.answer_media_group(media=read_photo('photo_corp_1_ind.txt'))
        return
    elif message.text == tl.name_button['about_us_2'][2]:
        text_list = read_text('about_corp_2.txt')
        for k in range(len(text_list)):
            await message.answer(text_list[k], parse_mode='Markdown')
        await message.answer_media_group(media=read_photo('photo_corp_2.txt'))
        return
    elif message.text == tl.name_button['about_us_2'][3]:
        text_list = read_text('about_apartments.txt')
        for k in range(len(text_list)):
            await message.answer(text_list[k], parse_mode='Markdown')
        await message.answer_media_group(media=read_photo('photo_apartments.txt'))
        return
    elif message.text == tl.name_button['about_us_2'][4]:
        text_list = read_text('about_cottage.txt')
        for k in range(len(text_list)):
            await message.answer(text_list[k], parse_mode='Markdown')
        await message.answer_media_group(media=read_photo('photo_cottage.txt'))
        return
    elif message.text == tl.name_button['about_us_2'][6]:
        await message.answer(read_text('int_answer_cat.txt', intr=True),
                             reply_markup=tl.create_button(key='booking_0'))
        await Def.booking.set()
    else:
        await message.answer(read_text('int_cancle.txt', intr=True),
                             reply_markup=tl.create_button(key='about_us_0'))
        await Def.about_us.set()


async def about_us_three_step(message: types.Message, state: FSMContext):
    """
    Logic bot.
    Tells about the hub.
    :param message:
    :param state:
    :return:
    """
    print(message)
    print(message.text)
    await lg.log_bot(message)
    if message.text not in tl.name_button['about_us_1']:
        await message.answer(read_text('int_not_button.txt', intr=True))
        return

    elif message.text == tl.name_button['about_us_1'][0]:
        text_list = read_text('about_hub.txt')
        for k in range(len(text_list)):
            await message.answer(text_list[k], parse_mode='Markdown')
        return

    elif message.text == tl.name_button['about_us_1'][1]:
        buttons = [
            types.InlineKeyboardButton(text='Наш адрес в Яндекс.Картах', url="https://yandex.ru/maps/pass"),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        await message.answer(read_text('other.txt', position=4),
                             reply_markup=keyboard)
        await message.answer_location(latitude=45.400709, longitude=36.968456,)
        return

    else:
        await message.answer(read_text('int_cancle.txt', intr=True),
                             reply_markup=tl.create_button(key='about_us_0'))
        await Def.about_us.set()


async def about_us_village(message: types.Message, state: FSMContext):
    """
    Logic bot.
    Tells about the village.
    :param message:
    :param state:
    :return:
    """
    print(message)
    print(message.text)
    await lg.log_bot(message)

    if message.text not in tl.name_button['about_us_3']:
        await message.answer(read_text('int_not_button.txt', intr=True))
        return

    elif message.text == tl.name_button['about_us_3'][0]:
        text_list = read_text('about_village_1.txt')
        for k in range(len(text_list)):
            await message.answer(text_list[k], parse_mode='Markdown')
        return

    elif message.text == tl.name_button['about_us_3'][1]:
        text_list = read_text('about_village_2.txt')
        for k in range(len(text_list)):
            await message.answer(text_list[k], parse_mode='Markdown')
        return

    else:
        await message.answer(read_text('int_cancle.txt', intr=True),
                             reply_markup=tl.create_button(key='about_us_0'))
        await Def.about_us.set()


def register_handlers_about_us(dp: Dispatcher):
    try:
        dp.register_message_handler(about_us_one_step, state=Def.about_us)
        dp.register_message_handler(about_us_two_step, state=About.about_room)
        dp.register_message_handler(about_us_three_step, state=About.about_way)
        dp.register_message_handler(about_us_village, state=About.about_village)
    except Exception:
        print('ERROR_about_us')