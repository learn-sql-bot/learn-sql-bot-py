from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.dispatcher.filters.state import State, StatesGroup
from states import ExerciseState
from dataprovider import DataProvider

async def cmd_select_topic(message: types.Message, state: FSMContext):

    # await state.set_state(ExerciseState.exercise_solving)
    topicname: str = message.text
    print(topicname)

    exercises = DataProvider.fetch_exercises_by_topic(topicname)

    if exercises:
        exercises_names: list = exercises.values()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*exercises_names)
        await state.update_data(topic=topicname)

        await message.answer("Выберите задачку, которую будете решать", reply_markup=keyboard)
        await state.set_state(ExerciseState.select_exercise)
    else:
        await message.answer("Не получилось, давайте снова попробуем")

async def cmd_select_exercise(message: types.Message, state: FSMContext):

    topic_name = await state.get_data()
    topic_name = topic_name.get("topic")

    exercise_name: str = message.text
    exercise_code: str = exercise_name.split(":")[0]

    exercise_sql: str = DataProvider.fetch_exercise_sql_by_topic_and_code(topic_name, exercise_code )
    exercise_text: str = DataProvider.fetch_exercise_text_by_topic_and_code(topic_name, exercise_code )

    await message.answer(f"Топик {topic_name} – Задача {exercise_code}")
    await message.answer(exercise_text)

    # await state.set_state(ExerciseState.exercise_solving)


# async def
# cmd_exercise_selection(message: types.Message, state: FSMContext):
#
#     await state.set_state(ExerciseState.exercise_solving)
#     await message.answer("Вот условие задачи")
#
#
# async def cmd_exercise_solving(message: types.Message, state: FSMContext):
#
#     await state.set_state(ExerciseState.exercise_checking)
#     await message.answer("Статус: ожидаем решения")
#
#
# async def cmd_exercise_checking(message: types.Message, state: FSMContext):
#
#     await state.set_state(ExerciseState.exercise_complete)
#     await message.answer("Отправляйте решение")
#
# async def cmd_exercise_complete(message: types.Message, state: FSMContext):
#
#     await message.answer("Задача решена выбирайте следующую")
#     await state.reset_state()

def register_handlers_exercise(dp: Dispatcher):
    dp.register_message_handler(cmd_select_topic, state=ExerciseState.select_topic)
    dp.register_message_handler(cmd_select_exercise, state=ExerciseState.select_exercise)
    # dp.register_message_handler(cmd_exercise_solving, state=ExerciseState.exercise_solving)
    # dp.register_message_handler(cmd_exercise_checking, state=ExerciseState.exercise_checking)
    # dp.register_message_handler(cmd_exercise_complete, state=ExerciseState.exercise_complete)
    # dp.register_message_handler(cmd_exercise_selection, state="*")

    # dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    # dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
    # dp.register_message_handler(secret_command, IDFilter(user_id=admin_id), commands="abracadabra")
