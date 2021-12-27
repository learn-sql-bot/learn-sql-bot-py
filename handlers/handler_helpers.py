import re

from aiogram import types
from aiogram.types import ReplyKeyboardMarkup

# Функции работы с интерфейсом телеграма
from aiogram.types.reply_keyboard import KeyboardButton


def build_keyboard(items: list, resize_keyboard: bool = True) -> ReplyKeyboardMarkup:
    """
    Собирает одноразовую клавиатурку для выбора категории
    :param items: список строк
    :param resize_keyboard: маленькие или большие кнопочки
    :return: объект айограма "клавиатура"
    """
    keyboard: ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(resize_keyboard=resize_keyboard, one_time_keyboard=True)
    keyboard.add(*items)
    return keyboard

def build_wide_keyboard(items: list) -> ReplyKeyboardMarkup:
    """
    Собирает одноразовую клавиатурку с клавишами на всю ширину экрана
    :param items: список строк
    :return: объект айограма "клавиатура"
    """

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for item in items:
        keyboard.add(KeyboardButton(item))
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


def parse_input_for_title(text: str) -> str:
    """
    Вытаскивает из строки название без номера
    :param text: Текст сообщения со скобочками
    :return: Возвращает номер категории в виде числа
    """

    title = text.split(" ", 1)[-1]
    return title
