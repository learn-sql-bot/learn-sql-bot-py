from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from classes.exercise import Exercise
from classes.sqlrunner import SQLRunnerResult
from handlers.handler_helpers import parse_input_for_id
from services.ExerciseService import ExerciseService
from states import ExerciseState
from classes.logger import Logger


class ExerciseHandler:

    def __init__(self):
        self.logger = Logger()
        self.exercise_service = ExerciseService()

    async def select_exercise(self, message: types.Message, state: FSMContext, ex_id=None):
        """ Обрабатываем команду выбора задания"""

        if not ex_id:
            input_text: str = message.text
            ex_id = parse_input_for_id(input_text)

        exercise = self.exercise_service.get_exercise_instruction(ex_id)

        if exercise:

            await self._send_exercise_instruction(message, exercise)
            await state.set_state(ExerciseState.exercise_solving)
            await state.set_data({"ex_id": ex_id})
            self.logger.log(f"Выбрано упражнение {ex_id}", message=message)

        else:
            await message.answer("Такого упражнения не нашлось, давайте еще раз?")
            self.logger.log(f"Попытка найти упражнение {ex_id}, не найдено", message=message)


    async def check_solution(self,message: types.Message, state: FSMContext):
        """ Обрабатываем отправленное решение """

        solution: str = message.text

        state_data = await state.get_data()
        ex_id = state_data.get("ex_id")

        if ex_id:

            self.logger.log(f"Запрошена проверка решения {ex_id}", message=message, state=state)

            user_result, solution_result = self.exercise_service.check_user_solution(ex_id, solution)

            if not user_result.errors:
                await message.answer(f"Запрос выполнен")
                await message.answer(f"``` \n{user_result.pretty} \n```", parse_mode="Markdown")
            else:
                await message.answer(f"Ошибка при выполнении")
                await message.answer("\n".join([str(e) for e in user_result.errors]), parse_mode="Markdown")
                return False

            if not user_result.columns == solution_result.columns:
                await message.answer(f"Колонки не совпадают")
                return False

            if not user_result.rows == solution_result.rows:
                await message.answer(f"Ряды не совпадают")
                return False

            await message.answer("Задача решена! Следующая: /next , В меню: /cats")
            # await state.reset_state()
            self.logger.log(f"Решена задача {ex_id}", message=message, state=state)
            return True

        else:
            await message.answer("Что то пошло не так, вернитесь к /cats")
            return False

    async def show_solution(self, message: types.Message, state: FSMContext):
        """ Показываем ответ если пользователь сдается """

        state_data = await state.get_data()
        ex_id: int = state_data.get("ex_id")

        exercise: Exercise = self.exercise_service.get_exercise_instruction(ex_id)

        await message.answer(f"Ответ на задачу {ex_id}:")
        await message.answer(exercise.sql_solution)

    async def show_example(self, message: types.Message, state: FSMContext):
        """ Показываем табличку ответ (кусочек)"""

        state_data = await state.get_data()
        ex_id = state_data.get("ex_id")
        result: SQLRunnerResult = self.exercise_service.show_example(ex_id)
        await message.answer(f"``` \n{result.pretty} \n```", parse_mode="Markdown")

    async def show_next(self, message: types.Message, state: FSMContext):
        """ Показываем табличку ответ (кусочек)"""

        state_data = await state.get_data()
        ex_id: int = state_data.get("ex_id")

        next_id: int = self.exercise_service.get_next_id_from_category(ex_id)

        if next_id:
            return await self.select_exercise(message, state, next_id)
        else:
            await message.answer(f"Это последнее упражнение, вернитесь к /cats")




    async def _send_exercise_instruction(self, message: types.Message, exercise: Exercise) -> None:

        await message.answer(exercise.title)
        await message.answer(exercise.instruction)
        await message.answer(f"``` \n{exercise.pretty} \n```", parse_mode="Markdown")
        await message.answer("Отправьте SQL в ответе, /show – показать ожидаемую табличку, /cats   меню, /ans – сдаться")




def register_handlers_exercise(dp: Dispatcher):

    x_handler = ExerciseHandler()

    dp.register_message_handler(x_handler.select_exercise, state=ExerciseState.select_exercise)

    dp.register_message_handler(x_handler.show_solution, commands="ans", state=ExerciseState.exercise_solving)
    dp.register_message_handler(x_handler.show_example, commands="show", state=ExerciseState.exercise_solving)
    dp.register_message_handler(x_handler.show_next, commands="next", state=ExerciseState.exercise_solving)

    dp.register_message_handler(x_handler.check_solution, state=ExerciseState.exercise_solving)

