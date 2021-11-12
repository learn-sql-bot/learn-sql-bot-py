import requests
import json

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from sqlrunner import SQLRunner

from handlers.common import register_handlers_common
from handlers.exercise import register_handlers_exercise


TOKEN = "2135086897:AAGV7_YafBfAjSSYcwRhqnEvFzTCNJuKf-o"


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

register_handlers_common(dp)
register_handlers_exercise(dp)






# @dp.message_handler()
# async def echo_message(message: types.Message):
#
#     query = message.text
#
#     dumpstring = requests.get("https://raw.githubusercontent.com/learn-sql-bot/learn-sql-bot/main/levels/level_1/content/task_1/data.sql").text
#     sqlrunner = SQLRunner()
#     sqlrunner.install_dump(dumpstring)
#     response = sqlrunner.run_query(query)
#     await message.reply(str(response))



if __name__ == '__main__':
    executor.start_polling(dp)
