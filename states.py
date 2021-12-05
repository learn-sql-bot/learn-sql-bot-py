from aiogram.dispatcher.filters.state import State, StatesGroup


class ExerciseState(StatesGroup):

    select_topic = State()
    select_exercise = State()
    exercise_solving = State()
    exercise_complete = State()
