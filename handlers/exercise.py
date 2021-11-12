from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.dispatcher.filters.state import State, StatesGroup
from states import ExerciseState


async def cmd_exercise_selection(message: types.Message, state: FSMContext):

    await state.set_state(ExerciseState.exercise_solving)
    await message.answer("Вот условие задачи")


async def cmd_exercise_solving(message: types.Message, state: FSMContext):

    await state.set_state(ExerciseState.exercise_checking)
    await message.answer("Статус: ожидаем решения")


async def cmd_exercise_checking(message: types.Message, state: FSMContext):

    await state.set_state(ExerciseState.exercise_complete)
    await message.answer("Отправляйте решение")

async def cmd_exercise_complete(message: types.Message, state: FSMContext):

    await message.answer("Задача решена выбирайте следующую")
    await state.reset_state()

def register_handlers_exercise(dp: Dispatcher):
    dp.register_message_handler(cmd_exercise_solving, state=ExerciseState.exercise_solving)
    dp.register_message_handler(cmd_exercise_checking, state=ExerciseState.exercise_checking)
    dp.register_message_handler(cmd_exercise_complete, state=ExerciseState.exercise_complete)
    dp.register_message_handler(cmd_exercise_selection, state="*")

    # dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    # dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
    # dp.register_message_handler(secret_command, IDFilter(user_id=admin_id), commands="abracadabra")
