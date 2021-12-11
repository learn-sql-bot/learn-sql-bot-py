import re

from aiogram import types
from aiogram.types import ReplyKeyboardMarkup

# Функции работы с интерфейсом телеграма


def build_keyboard(items: list) -> ReplyKeyboardMarkup:
    """
    Собирает одноразовую клавиатурку для выбора категории
    :param items: список строк
    :return: объект айограма "клавиатура"
    """
    keyboard: ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*items)
    return keyboard


# Функции парсинга ответа пользователя


def parse_input_for_id(text: str) -> int:
    """
    Вытаскивает из строки завернутый в скобочки номер
    :param text: Текст сообщения со скобочками
    :return: Возвращает номер категории в виде числа
    """
    p: re.Pattern = re.compile(r'\[(.*?)\]')
    number: int = int(p.findall(text)[0])
    return number

