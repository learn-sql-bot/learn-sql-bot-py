from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from handlers.common import register_handlers_common
from handlers.exercise import register_handlers_exercise
from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

### Регистируем обработчики

register_handlers_common(dp)
register_handlers_exercise(dp)


if __name__ == '__main__':
    executor.start_polling(dp)
