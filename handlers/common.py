from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
import requests

from states import ExerciseState
from sqlrunner import SQLRunner


async def cmd_start(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer("Привет! Начнем что нибудь решать?")


async def cmd_test(message: types.Message, state: FSMContext):

    dumpstring: requests.models.Response = requests.get("https://raw.githubusercontent.com/learn-sql-bot/learn-sql-bot/main/levels/level_1/content/task_1/data.sql").text
    sqlrunner = SQLRunner()
    sqlrunner.install_dump(dumpstring)
    query: str = "SELECT * from user_details"
    response: list = sqlrunner.run_query(query)
    await message.reply(str(response))



def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state=ExerciseState)
    dp.register_message_handler(cmd_test, commands="test", state="*")

    # dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    # dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
    # dp.register_message_handler(secret_command, IDFilter(user_id=admin_id), commands="abracadabra")
