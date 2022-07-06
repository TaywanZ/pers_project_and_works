from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from inside_function.text_read import read_text
from dict.menu import Step, Def, main_menu
import inside_function.logic_bot as lg
import inside_function.tele_logic as tl
import inside_function.chek_booking as chek
import inside_function.config as conf


class Booking(StatesGroup):
    date_in = State()
    count_in = State()
    add_bk = State()
    false_add_bk = State()


async def booking_one(message: types.Message, state: FSMContext):
    print(message)
    print(message.text)
    await lg.log_bot(message)
    if message.text not in tl.name_button['booking_0']:
        await message.answer(read_text('int_not_button.txt', intr=True))
        return
    elif message.text == tl.name_button['booking_0'][0]:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('Отмена бронирования')
        await message.answer(read_text('booking.txt', position=0), reply_markup=keyboard)
        await Booking.count_in.set()
    else:
        await message.answer(read_text('int_cancle.txt', intr=True))
        await Step.step_0.set()
        await main_menu(message, state)


async def choice_count(message: types.Message, state: FSMContext):
    print(message)
    print(message.text)
    await lg.log_bot(message)
    if message.text == 'Отмена бронирования':
        await message.answer(read_text('int_cancle.txt', intr=True))
        await state.finish()
        await Step.step_0.set()
        await main_menu(message, state)
    else:
        try:
            count_client = int(message.text)
        except:
            await message.answer('Введено не число!\nПовторите ввод.')
            return

        await state.update_data(client_count=count_client)
        await message.answer(read_text('booking.txt', position=1))
        await Booking.date_in.set()


async def choice_date(message: types.Message, state: FSMContext):
    print(message)
    print(message.text)
    await lg.log_bot(message)
    if message.text == 'Отмена бронирования':
        await message.answer(read_text('int_cancle.txt', intr=True))
        await Step.step_0.set()
        await main_menu(message, state)
    else:
        flag = lg.this_date(message.text)
        if flag[0]:
            await state.update_data(date_in=flag[1], date_out=flag[2])
            data = await state.get_data()
            disclamer = await message.answer('Ищу подходящие варианты, это займёт пару секунд')
            text, button_name, data_serv = chek.chek_room(data['date_in'], data['date_out'], data['client_count'])
            await disclamer.delete()
            if button_name:
                await message.answer(read_text('booking.txt', position=2))
                await message.answer(text)
                await message.answer(read_text('booking.txt', position=3),
                                     parse_mode='Markdown',
                                     reply_markup=(tl.create_button(list_button=button_name)
                                                   .add('Выбрать другие даты')
                                                   .add('Отмена бронирования')))
                await state.update_data(input_data=data_serv, list_button=button_name)
                await Booking.add_bk.set()
            else:
                try:
                    list_buttons, text = chek.false_price(data['date_in'], data['date_out'])
                    await message.answer(text)
                    await message.answer(read_text('booking.txt', position=5),
                                         parse_mode='Markdown',
                                         reply_markup=(tl.create_button(list_button=list_buttons)
                                                       .add('Выбрать другие даты')
                                                       .add('Отмена бронирования')))
                    await state.update_data(input_data=text, list_button=list_buttons)
                    await Booking.false_add_bk.set()
                except:
                    await message.answer(read_text('booking.txt', position=8))
                    return
        else:
            await message.answer(flag[1])
            return


async def choice_rooms(message: types.Message, state: FSMContext):
    print(message)
    print(message.text)
    await lg.log_bot(message)
    data = await state.get_data()
    list_rooms = data['list_button']

    if message.text == 'Отмена бронирования':
        await message.answer(read_text('int_cancle.txt', intr=True))
        await state.finish()
        await Step.step_0.set()
        await main_menu(message, state)

    elif message.text == 'Выбрать другие даты':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('Отмена бронирования')
        await message.answer(read_text('booking.txt', position=1), reply_markup=keyboard)
        await Booking.date_in.set()

    elif message.text in list_rooms:
        if message.chat.username and not message.from_user.is_bot:
            config = conf.load_config(flag=1)
            str_bokking = str()
            keys = ['date_in', 'date_out', 'client_count']
            for kay in keys:
                str_bokking += kay + '\t:\t' + str(data[kay]) + '\n'
            str_bokking += 'Choice_room:\t' + message.text + '\n'
            for keys in data['input_data']:
                if message.text == data['input_data'][keys]['name']:
                    id_corp = keys
                    str_bokking += 'Price:\t' + str(data['input_data'][id_corp]['plans_price']) + '\n'
                    str_bokking += 'Name client:\t' + message.chat.first_name

            if chek.data_to_send(message, data):
                await message.answer(read_text('booking.txt', position=4))
                await bot.send_message(config.admin_id[config.active_admin],
                                       text=f'Новая бронь от: @{message["chat"]["username"]}')
                await bot.send_message(config.admin_id[config.active_admin], str_bokking)
                await state.finish()
                await Step.step_0.set()
                await main_menu(message, state)
            else:
                await message.answer(read_text('booking.txt', position=7))
                await bot.send_message(config.admin_id[config.active_admin],
                                       text=f'Новая бронь С ОШИБКОЙ от: @{message["chat"]["username"]}')
                await bot.send_message(config.admin_id[config.active_admin], str_bokking)
                await state.finish()
                await Step.step_0.set()
                await main_menu(message, state)
        else:
            await message.answer(read_text('not_username.txt', position=1))
            return


async def false_choice_rooms(message: types.Message, state: FSMContext):
    print(message)
    print(message.text)
    await lg.log_bot(message)
    data = await state.get_data()
    list_rooms = data['list_button']

    if message.text == 'Отмена бронирования':
        await message.answer(read_text('int_cancle.txt', intr=True))
        await state.finish()
        await Step.step_0.set()
        await main_menu(message, state)

    elif message.text == 'Выбрать другие даты':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('Отмена бронирования')
        await message.answer(read_text('booking.txt', position=1), reply_markup=keyboard)
        await Booking.date_in.set()

    elif message.text in list_rooms:
        if message.chat.username:
            config = conf.load_config(flag=1)
            str_bokking = str()
            keys = ['date_in', 'date_out', 'client_count']
            for kay in keys:
                str_bokking += kay + '\t:\t' + str(data[kay]) + '\n'
            str_bokking += 'Choice_room:\t' + message.text + '\n'
            text = data['input_data'].split('\n')
            for tx in text:
                tx = tx.split('\t:\t')
                if tx[0] == message.text:
                    str_bokking += 'Price:\t' + str(tx[1]) + '\n'
            str_bokking += 'Name client:\t' + message.chat.first_name
            await message.answer(read_text('booking.txt', position=6))
            await bot.send_message(config.admin_id[config.active_admin],
                                   text=f'Новая ЗАЯВКА НА БРОНЬ от пользователя: @{message["chat"]["username"]}')
            await bot.send_message(config.admin_id[config.active_admin], str_bokking)
            await state.finish()
            await Step.step_0.set()
            await main_menu(message, state)
        else:
            await message.answer(read_text('not_username.txt', position=1))
            return


def register_handlers_booking(dp: Dispatcher):
    try:
        dp.register_message_handler(booking_one, state=Def.booking)
        dp.register_message_handler(choice_date, state=Booking.date_in)
        dp.register_message_handler(choice_count, state=Booking.count_in)
        dp.register_message_handler(choice_rooms, state=Booking.add_bk)
        dp.register_message_handler(false_choice_rooms, state=Booking.false_add_bk)
        global bot
        bot = dp.bot
    except Exception:
        pass