import re

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

import config
from states import ExerciseState
from services.ExerciseService import ExerciseService


def parse_input_for_id(text: str) -> int:   # TODO вынести в хелперы или  отдельные функцйии общие для категорий и упражнений
    """
    Вытаскивает из строки завернутый в скобочки номер
    :param text: Текст сообщения со скобочками
    :return: Возвращает омер категории в виде числа
    """
    p = re.compile(r'\[(.*?)\]')
    number = int(p.findall(text)[0])
    return number


async def cmd_select_exercise(message: types.Message, state: FSMContext):
    """ Обрабатываем команду выбора задания"""

    input_text: str = message.text
    ex_id = parse_input_for_id(input_text)

    exercise_service = ExerciseService()
    exercise = exercise_service.get_exercise_instruction(ex_id)

    if exercise:  # TODO тут переписать на хелперы или выгнести в сервисы
        await message.answer(exercise.get("title"))
        await message.answer(exercise.get("instruction"))
        await message.answer(f"``` \n{exercise.get('pretty')} \n```", parse_mode="Markdown")
        await message.answer("Отправьте SQL в ответе, /show – показать ожидаемую табличку, /cats   меню, /ans – сдаться")
        await state.set_state(ExerciseState.exercise_solving)
        await state.set_data({"ex_id": ex_id})
    else:
        await message.answer("Такого упражнения не нашлось, давайте еще раз?")

    if config.DEBUG:
        await message.answer(f"state: { await state.get_state()}")


async def cmd_check_solution(message: types.Message, state: FSMContext):
    """ Обрабатываем отправленное решение """

    solution: str = message.text
    exercise_service = ExerciseService()
    state_data = await state.get_data()
    ex_id = state_data.get("ex_id")

    if ex_id:

        user_result, solution_result = exercise_service.check_user_solution(ex_id, solution)

        if not user_result.errors:
            await message.answer(f"Запрос выполнен")
            await message.answer(f"``` \n{user_result.pretty} \n```", parse_mode="Markdown")
        else:
            await message.answer(f"Ошибка при выполнении")
            await message.answer("\n".join([str(e) for e in user_result.errors]), parse_mode="Markdown")
            return Falst

        if not user_result.columns == solution_result.columns:
            await message.answer(f"Колонки не совпадают")
            return False

        if not user_result.rows == solution_result.rows:
            await message.answer(f"Ряды не совпадают")
            return False

        await message.answer("Задача решена выбирайте следующую /cats")
        await state.reset_state()
        return True

    else:
        await message.answer("Что то пошло не так, вернитесь к /cats")
        return False


async def cmd_show_solution(message: types.Message, state: FSMContext):
    """ Показываем ответ если пользователь сдается """

    exercise_service = ExerciseService()
    state_data = await state.get_data()
    ex_id = state_data.get("ex_id")
    exercise = exercise_service.get_exercise_instruction(ex_id)

    await message.answer(f"Ответ на задачу {ex_id}:")
    await message.answer(exercise.get("sql_solution"))


def register_handlers_exercise(dp: Dispatcher):

    dp.register_message_handler(cmd_select_exercise, state=ExerciseState.select_exercise)
    dp.register_message_handler(cmd_show_solution, commands="ans", state=ExerciseState.exercise_solving)
    dp.register_message_handler(cmd_check_solution, state=ExerciseState.exercise_solving)

