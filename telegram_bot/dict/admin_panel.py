from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IDFilter
from aiogram.dispatcher.filters.state import State, StatesGroup
from dict.menu import Def, main_menu, Step
from inside_function.text_read import read_text, list_text, list_photo, read_photo
from inside_function.rw_feedback import read_feedback, write_feedback
from pathlib import Path
import inside_function.config as conf
import inside_function.tele_logic as tl
import inside_function.logic_bot as lg
import asyncio



class Admin(StatesGroup):
    mass_message = State()
    replace_text_one = State()
    replace_text_two = State()
    replace_photo_one = State()
    replace_photo_two = State()
    active_adm = State()


async def admin_mode_one_step(message: types.Message, state: FSMContext):
    """
    Logic bot.
    Calls special function for the admin.
    :param message:
    :param state:
    :return:
    """
    await lg.log_bot(message)
    print(message)
    print(message.text)
    if message.text not in tl.name_button['admin_panel']:
        await message.answer(read_text('int_not_button.txt', intr=True))
        return
    elif message.text == tl.name_button['admin_panel'][0]:
        await message.answer(read_text('other.txt', position=5))
        await Admin.mass_message.set()
    elif message.text == tl.name_button['admin_panel'][1]:
        await message.answer(lg.static_data())
        return
    elif message.text == tl.name_button['admin_panel'][2]:
        list_button = list_text()
        await message.answer(read_text('other.txt', position=8),
                             reply_markup=tl.create_button(list_button=list_button).add('Отмена'))
        await Admin.replace_text_one.set()
    elif message.text == tl.name_button['admin_panel'][3]:
        list_button = list_photo()
        await message.answer(read_text('other.txt', position=8),
                             reply_markup=tl.create_button(list_button=list_button).add('Отмена'))
        await Admin.replace_photo_one.set()
    elif message.text == tl.name_button['admin_panel'][4]:
        config = conf.load_config(flag=1)
        list_button = config.admin_name
        await message.answer(read_text('other.txt', position=10),
                             reply_markup=tl.create_button(list_button=list_button).add('Отмена'))
        await Admin.active_adm.set()
    else:
        await message.answer(read_text('int_cancle.txt', intr=True))
        await Step.step_0.set()
        await main_menu(message, state)


async def active_admins(message: types.Message, state: FSMContext):
    print(message)
    print(message.text)
    await lg.log_bot(message)
    config = conf.load_config(flag=1)
    list_button = config.admin_name
    k = list_button.index(message.text)
    print(k)
    if conf.write_config(k):
        await message.answer(f'Активный админ успешно изменён на @{config.admin_name[k]}')
        await bot.send_message(config.admin_id[k], 'Вы назначены активным админом!')
        await Step.step_0.set()
        await main_menu(message, state)
    else:
        await message.answer('Ошибка, попробуйте сменить активного админа вручную.')


async def admin_mass(message: types.Message, state: FSMContext):
    """
    Logic bot.
    Gets mass message text and performs mass mailing.
    :param message:
    :param state:
    :return:
    """
    print(message)
    print(message.text)
    await lg.log_bot(message)
    list_user = lg.all_user()
    count_bed = 0
    count_good = 0
    for chat in list_user:
        try:
            await bot.send_message(chat_id=chat, text=message.text)
            count_good += 1
            await asyncio.sleep(.05)
        except:
            count_bed += 1
            continue
    await message.answer(f'Успешных отправок: {count_good}.\nОтправок с ошибкой: {count_bed}')
    await Def.admin_mode.set()


async def replace_text_file(message: types.Message, state: FSMContext):
    """
    Logic bot.
    Gets name text file. Return text from a file.
    :param message:
    :param state:
    :return:
    """
    print(message)
    print(message.text)
    await lg.log_bot(message)
    if message.text == 'Отмена':
        await message.answer(read_text('int_cancle.txt', intr=True))
        await Step.step_0.set()
        await main_menu(message, state)
    else:
        await state.update_data(name_text=message.text)
        await message.answer(read_feedback(name_text=message.text))
        await Admin.replace_text_two.set()


async def replace_text_file_two(message: types.Message, state: FSMContext):
    """
    Gets new text for the file. Replaces text in the file
    :param message:
    :param state:
    :return:
    """
    print(message)
    print(message.text)
    text = message.text
    message.text = 'Изменение файла'
    await lg.log_bot(message)
    name_f = await state.get_data()
    k = write_feedback(text, name_text=name_f['name_text'])
    if k:
        text = read_text(name_f['name_text'])
        for k in range(len(text)):
            await message.answer(text[k])
    else:
        await message.answer('Ошибка')
    await state.finish()
    await Step.step_0.set()
    await main_menu(message, state)


async def replace_photo_one(message: types.Message, state: FSMContext):
    """
        Logic bot.
        Gets name photo file. Return text from a file.
        :param message:
        :param state:
        :return:
        """
    print(message)
    print(message.text)
    await lg.log_bot(message)
    if message.text == 'Отмена':
        await message.answer(read_text('int_cancle.txt', intr=True))
        await Step.step_0.set()
        await main_menu(message, state)
    else:
        list_button = ['Сохранить правки', 'Отмена']
        await state.update_data(name_file=message.text, id_photo=[])
        await message.answer_media_group(media=read_photo(message.text))
        await message.answer(read_text('other.txt', position=11),
                             reply_markup=tl.create_button(list_button=list_button))
        await Admin.replace_photo_two.set()


async def replace_photo_two(message: types.Message, state: FSMContext):
    data = await state.get_data()
    photo_id = message.photo[-1].file_id
    photo = data['id_photo']
    photo.append(photo_id)
    print(photo)
    await state.update_data(id_photo=photo)


async def replace_photo_three(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer(read_text('int_cancle.txt', intr=True))
        await Step.step_0.set()
        await main_menu(message, state)
    else:
        data = await state.get_data()
        photo = str()
        for i in range(len(data['id_photo'])):
            if i == len(data['id_photo']) - 1:
                photo += data['id_photo'][i]
            else:
                photo += data['id_photo'][i] + '\n'
        path = Path(Path.cwd(), 'photo', data['name_file'])
        with open(path, 'w', newline='') as fl:
            fl.write(photo)
            fl.close()
        await message.answer_media_group(media=read_photo(data['name_file']))
        await state.finish()
        await Step.step_0.set()
        await main_menu(message, state)


def register_handlers_admin_mode(dp: Dispatcher, admin_id: list):
    try:
        dp.register_message_handler(admin_mode_one_step, IDFilter(user_id=admin_id), state=Def.admin_mode)
        dp.register_message_handler(admin_mass, state=Admin.mass_message)
        dp.register_message_handler(replace_text_file, state=Admin.replace_text_one)
        dp.register_message_handler(replace_text_file_two, state=Admin.replace_text_two)
        dp.register_message_handler(active_admins, state=Admin.active_adm)
        dp.register_message_handler(replace_photo_one, state=Admin.replace_photo_one)
        dp.register_message_handler(replace_photo_two, content_types=types.ContentType.PHOTO, state=Admin.replace_photo_two)
        dp.register_message_handler(replace_photo_three, content_types=types.ContentType.TEXT, state=Admin.replace_photo_two)
        global bot
        bot = dp.bot
    except Exception:
        pass
