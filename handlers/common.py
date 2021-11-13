from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter


from states import ExerciseState
from sqlrunner import SQLRunner
from dataprovider import DataProvider, DataProviderLocal
from classes.exercise import Exercise


async def cmd_table(message: types.Message, state: FSMContext):

    sqlrunner = SQLRunner()
    sql_dump: str = DataProvider.fetch_exercise_sql_by_topic_and_code("SELECT", "A01")
    sqlrunner.install_dump(sql_dump)

    # result = sqlrunner.run_query(".tables")

    sqlrunner.run_query("SELECT user_id, username, first_name, last_name from `user_details`")
    table: str = sqlrunner.get_prettytable()
    await message.answer(f"``` \n{table} \n```", parse_mode="Markdown")




async def cmd_test(message: types.Message, state: FSMContext):

    topic: str = "SELECT"
    code: str = "A01"
    data_provider = DataProviderLocal()
    exercise = data_provider.get_exercise_by_topic_and_code(topic, code)
    exercise.install_dump()

    pretty: str = exercise.get_pretty()
    text: str = exercise.get_text()

    await message.answer(f"{topic} {code}")
    await message.answer(text)
    await message.answer(pretty, parse_mode="Markdown")



def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_table, commands="table", state="*")
    dp.register_message_handler(cmd_test, commands="test", state="*")

    # dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    # dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
    # dp.register_message_handler(secret_command, IDFilter(user_id=admin_id), commands="abracadabra")
