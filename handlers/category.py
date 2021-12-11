from typing import List

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

import config
from classes.category import Category
from classes.exercise import Exercise
from handlers.handler_helpers import build_keyboard, parse_input_for_id
from services.CategoryService import CategoryService
from states import ExerciseState


async def cmd_all_categories(message: types.Message, state: FSMContext):
    """ Обрабатываем команду /cats, отдаем список всех категорий """

    # Получаем список всех категорий
    category_service: CategoryService = CategoryService()
    cats: List[Category] = category_service.all_categories()

    # строим клавиатуру из названий всех полученных категорий
    keyboard = build_keyboard([f"{cat.title} [{cat.id}]" for cat in cats])

    # Отправляем список пользователю
    await message.answer(f"Все категории",  reply_markup=keyboard, parse_mode="Markdown")

    # Переходим в режим прием
    await state.set_state(ExerciseState.select_topic)

    if config.DEBUG:
        await message.answer(f"state: { await state.get_state()}")


async def cmd_get_single_category(message: types.Message, state: FSMContext):
    """ Обрабатываем выбор варианта категори"""

    # Подключаем бизнес логику
    category_service = CategoryService()

    # Обрабатываем ввод и вытаскиваем цифру из скобочек
    input_text: str = message.text
    cat_id: int = parse_input_for_id(input_text)

    category: Category = category_service.get_category(cat_id)

    exercises: List[Exercise] = category.exercises

    # Если упражнение какое нибудь есть
    if exercises:

        keyboard = build_keyboard([f"{e.title} [{e.id}]" for e in exercises])
        await message.answer(
            f"Все задания на тему { category.title }",
            reply_markup=keyboard,
            parse_mode="Markdown")

        # Переходим в режим выбора упражнения
        await state.set_state(ExerciseState.select_exercise)

    else:
        await message.answer(f"Заданий в этой категории пока нет, выберите другую")

    if config.DEBUG:
        await message.answer(f"state: { await state.get_state()}")


def register_handlers_category(dp: Dispatcher):

    # Обрабатывать запрос /cats и показывать категории
    dp.register_message_handler(cmd_all_categories, commands="cats", state="*")
    dp.register_message_handler(cmd_all_categories, commands="start", state="*")
    # Обрабатывать запрос на показывание одной категории
    dp.register_message_handler(cmd_get_single_category,  state=ExerciseState.select_topic)

