from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter

from states import ExerciseState
from sqlrunner import SQLRunner
from dataprovider import DataProvider


async def cmd_start(message: types.Message, state: FSMContext):

    topics: dict = DataProvider.fetch_topics()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*topics.keys())
    await message.answer("Привет! Что будем учить сегодня?", reply_markup=keyboard)
    await state.set_state(ExerciseState.select_topic)


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")

