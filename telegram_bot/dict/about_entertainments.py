from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from dict.menu import Step, Def, main_menu
from inside_function.text_read import read_text, read_photo
import inside_function.logic_bot as lg
import inside_function.tele_logic as tl


class Activiti(StatesGroup):
    what_activiti = State()


async def entertainments_one(message: types.Message, state: FSMContext):
    print(message)
    print(message.text)
    await lg.log_bot(message)
    if message.text not in tl.name_button['about_e']:
        await message.answer(read_text('int_not_button.txt', intr=True))
        return
    elif message.text == tl.name_button['about_e'][0]:
        text_list = read_text('about_partying.txt')
        for k in range(len(text_list)):
            await message.answer(text_list[k])
        await message.answer_media_group(media=read_photo('photo_party.txt'))
        return
    elif message.text == tl.name_button['about_e'][1]:
        text_list = read_text('about_animate.txt')
        for k in range(len(text_list)):
            await message.answer(text_list[k])
        await message.answer_media_group(media=read_photo('photo_animation.txt'))
        return
    elif message.text == tl.name_button['about_e'][2]:
        text_list = read_text('about_excursion.txt')
        for k in range(len(text_list)):
            await message.answer(text_list[k])
        return
    elif message.text == tl.name_button['about_e'][3]:
        text_list = read_text('about_attractions.txt')
        for k in range(len(text_list)):
            await message.answer(text_list[k])
        return
    else:
        await message.answer(read_text('int_cancle.txt', intr=True))
        await Step.step_0.set()
        await main_menu(message, state)


def register_handlers_entertainments(dp: Dispatcher):
    try:
        dp.register_message_handler(entertainments_one, state=Def.entertainments)
    except Exception:
        print('ERROR_abount_est')