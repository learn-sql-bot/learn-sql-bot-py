import re
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from states import ExerciseState
from services.CategoryService import CategoryService
import config


def build_keyboard(items):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*items)
    return keyboard


def parse_input_for_id(text:str) -> int:
    p = re.compile(r'\[(.*?)\]')
    number = int(p.findall(text)[0])
    return number

async def cmd_all_categories(message: types.Message, state: FSMContext):
    """ Обрабатываем команду /cats, отдаем список всех категорий """

    # Получаем список всех категорий
    category_service = CategoryService()
    cats = category_service.all_categories()

    # строим клавиатуру из названий всех полученных категорий
    keyboard = build_keyboard([f"{cat.get('title')} [{cat.get('id')}]" for cat in cats])


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
    cat_id = parse_input_for_id(input_text)

    category = category_service.get_category(cat_id)
    category_exercises = category.get("exercises")

    # Если упражнение какое нибудь есть
    if category_exercises:

        keyboard = build_keyboard([f"{e.get('title')} [{e.get('id')}]" for e in category_exercises])
        await message.answer(f"Все задания на тему { category.get('title') }",  reply_markup=keyboard, parse_mode="Markdown")

        # Переходим в режим выбора упражнения
        await state.set_state(ExerciseState.select_exercise)

    else:
        await message.answer(f"Заданий в этой категории пока нет, выберите другую")

    if config.DEBUG:
        await message.answer(f"state: { await state.get_state()}")



def register_handlers_category(dp: Dispatcher):
    dp.register_message_handler(cmd_all_categories, commands="cats", state="*")
    dp.register_message_handler(cmd_get_single_category,  state=ExerciseState.select_topic)
