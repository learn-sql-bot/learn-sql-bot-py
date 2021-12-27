from aiogram import types
from aiogram.types import ReplyKeyboardMarkup
from typing import List

from classes.category import Category


class ResponseFormatter:
    """
    Форматирует ответы и готовит сообщения для отправки пользователю
    """

    def __init__(self):
        pass

    def all_categories(self, categories: List[Category]) -> tuple:
        """
         # собираем текстовый ответ на запрос всех категорий
        """

        response = ["Выберите тему, которая вам нравится"]
        # [response.append(f"{i}  {cat.title}") for i, cat in enumerate(categories, 1)]

        keyboard: ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(*[f"{i} {cat.title}" for i, cat in enumerate(categories, 1)])

        return "\n".join(response), keyboard


    def single_category(self, category: Category) -> tuple:
        """
        Форматирует ответ на запрос категории
        """

        # собираем текстовый ответ
        print(category)
        response = [category.title, ""]
        [response.append(f"{i} {ex.title}") for i, ex in enumerate(category.exercises, 1)]

        # собираем клавиатуру

        keyboard: ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(*[str(i) for i in range(1, len(category.exercises) + 1)])

        return "\n".join(response), keyboard

    def _format_keybord(self):
        pass
