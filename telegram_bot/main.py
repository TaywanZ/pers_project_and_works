from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
import asyncio
import inside_function.config as conf
from dict.menu import register_handlers_main_menu
from dict.about_us import register_handlers_about_us
from dict.about_entertainments import register_handlers_entertainments
from dict.admin_panel import register_handlers_admin_mode
from dict.booking import register_handlers_booking


async def main():
    """
    Launching the bot
    :return:
    """

    config = conf.load_config(flag=0)
    config_admin = conf.load_config(flag=1)

    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=config.token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_main_menu(dp)
    register_handlers_about_us(dp)
    register_handlers_entertainments(dp)
    register_handlers_admin_mode(dp, config_admin.admin_id)
    register_handlers_booking(dp)

    # Запуск поллинга
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
