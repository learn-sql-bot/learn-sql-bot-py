import sqlite3
from sqlite3 import Connection, Cursor

from typing import List

from classes.exercise import Exercise
from config import DBPATH


class ExerciseDataProvider:
    """ Поставщик данных об упражнениях """

    def __init__(self, db_path=None):

        if not db_path:
            db_path = DBPATH

        # Подключаемся к БД
        self.connect: Connection = sqlite3.connect(db_path)

        # Запускаем курсор, с помощью которого мы будем получать данные из БД
        self.cur = self.connect.cursor()

    def get_by_id(self, ex_id: int) -> Exercise:
        """ Возвращает объект упражнения по его id"""

        query: str = f"SELECT id, title, instruction, sql_base, sql_solution, tables " \
                     f"FROM exercises " \
                     f"WHERE id = { ex_id } " \
                     f"LIMIT 1"

        self.cur.execute(query)
        exercise_data: list = self.cur.fetchone()
        exercise: Exercise = Exercise(*exercise_data)
        exercise.tables = [table.strip() for table in exercise.sql_tables.strip().split(",")]

        return exercise

    def get_by_category(self, cat_id: int) -> List[Exercise]:

        """ Возвращает упражнения из категории по ее id в формате списка словарей """

        query: str = f"SELECT `id`, `title`, `instruction`" \
                     f"FROM exercises " \
                     f"WHERE category = { cat_id } " \
                     f"ORDER by `order`"

        result: Cursor = self.cur.execute(query)
        exercises_data: list = self.cur.fetchall()
        exercises = [Exercise(*ex) for ex in exercises_data]

        return exercises




