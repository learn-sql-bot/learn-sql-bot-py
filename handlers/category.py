from typing import List

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

import config
from classes.category import Category
from classes.exercise import Exercise
from classes.logger import Logger
from handlers.handler_helpers import build_keyboard, build_wide_keyboard, parse_input_for_title
from services.CategoryService import CategoryService
from services.ResponseFormatter import ResponseFormatter
from states import ExerciseState


class CategoryHandler:

    def __init__(self):
        self.logger = Logger()
        self.category_service = CategoryService()
        self.formatter = ResponseFormatter()

    async def all_categories(self, message: types.Message, state: FSMContext):
        """ Обрабатываем команду /cats, отдаем список всех категорий """

        self.logger.log(f"Запрошен список категорий ", message=message, state=state)

        # Получаем список всех категорий
        cats: List[Category] = self.category_service.all_categories()

        # собираем сообщение и клавиатуру
        response, keyboard = self.formatter.all_categories(cats)

        # Отправляем ответ пользователю
        await message.answer(response,  reply_markup=keyboard, parse_mode="Markdown")

        # Переходим в режим прием
        await state.set_state(ExerciseState.select_topic)



    async def get_single_category(self, message: types.Message, state: FSMContext):
        """ Обрабатываем выбор варианта категории
        Выводим описание категории и список заданий
        """

        self.logger.log(f"Запрошены задачи категории {message.text}", message=message, state=state)

        # Обрабатываем ввод и вытаскиваем название
        cat_title: str = parse_input_for_title(message.text)

        # Получаем датакласс категории
        category: Category = self.category_service.get_category_by_title(cat_title)

        await state.set_data({"cat_id": category.id})

        # Если упражнение какое нибудь есть

        if category.exercises:

            # Выводим упражнения с кнопочками
            response, keyboard = self.formatter.single_category(category)
            # Переходим в режим выбора упражнения
            await state.set_state(ExerciseState.select_exercise)

            # Отправляем ответ пользователю
            await message.answer(response,  reply_markup=keyboard, parse_mode="Markdown")

        else:

            await message.answer(f"Заданий в этой категории пока нет, выберите другую")




def register_handlers_category(dp: Dispatcher):

    c_handler = CategoryHandler()

    # Обрабатывать запрос /cats и показывать категории
    dp.register_message_handler(c_handler.all_categories, commands="cats", state="*")
    dp.register_message_handler(c_handler.all_categories, commands="start", state="*")
    # Обрабатывать запрос на показывание одной категории
    dp.register_message_handler(c_handler.get_single_category,  state=ExerciseState.select_topic)

