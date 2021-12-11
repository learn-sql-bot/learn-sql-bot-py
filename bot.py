from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN
from handlers.category import register_handlers_category
from handlers.exercise import register_handlers_exercise


def create_bot(token=None):

    bot: Bot = Bot(token)
    dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())

    ### Регистируем обработчики

    register_handlers_category(dp)
    register_handlers_exercise(dp)

    return bot, dp


def run(executor, dp):

    print("bot is running")
    executor.start_polling(dp)  # начинаем получать запросики


bot, dp = create_bot(TOKEN)

if __name__ == '__main__':
    run(executor, dp)
