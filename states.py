from aiogram.dispatcher.filters.state import State, StatesGroup


class ExerciseState(StatesGroup):

    exercise_selection = State()
    exercise_solving = State()
    exercise_checking = State()
    exercise_complete = State()
