from typing import List

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

import config
from classes.category import Category
from classes.exercise import Exercise
from classes.logger import Logger
from handlers.handler_helpers import build_keyboard, parse_input_for_id
from services.CategoryService import CategoryService
from states import ExerciseState


class CategoryHandler:

    def __init__(self):
        self.logger = Logger()

    async def all_categories(self, message: types.Message, state: FSMContext):
        """ Обрабатываем команду /cats, отдаем список всех категорий """

        self.logger.log(f"Запрошен список категорий ", message=message, state=state)

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

    async def get_single_category(self, message: types.Message, state: FSMContext):
        """ Обрабатываем выбор варианта категори"""

        # Подключаем бизнес логику
        category_service = CategoryService()

        # Обрабатываем ввод и вытаскиваем цифру из скобочек
        input_text: str = message.text
        cat_id: int = parse_input_for_id(input_text)

        self.logger.log(f"Запрошены задачи категории {cat_id}", message=message, state=state)

        category: Category = category_service.get_category(cat_id)

        await state.set_data({"cat_id": cat_id})

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




def register_handlers_category(dp: Dispatcher):

    c_handler = CategoryHandler()

    # Обрабатывать запрос /cats и показывать категории
    dp.register_message_handler(c_handler.all_categories, commands="cats", state="*")
    dp.register_message_handler(c_handler.all_categories, commands="start", state="*")
    # Обрабатывать запрос на показывание одной категории
    dp.register_message_handler(c_handler.get_single_category,  state=ExerciseState.select_topic)

