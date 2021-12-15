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

    def get_next_id_from_category(self, ex_id: int) -> int:

        """ Возвращает номер следующего упражнения из категории, основываясь на order
            Если такого упражнения нет (например, это было последнее), возвращает 0
        """

        query: str = f"SELECT `category` from `exercises` where `id` = { ex_id }"
        self.cur.execute(query)
        exercise_data: tuple = self.cur.fetchone()
        cat_id = exercise_data[0] if exercise_data else 0

        query: str = f"SELECT `id` " \
                     f"FROM exercises " \
                     f"WHERE category = { cat_id } " \
                     f"AND `order` > (SELECT `order` FROM exercises where `id` = { ex_id }) " \
                     f"ORDER by `order` " \


        self.cur.execute(query)
        next_data: tuple = self.cur.fetchone()
        next_id: int = int(next_data[0]) if next_data else 0

        return next_id

