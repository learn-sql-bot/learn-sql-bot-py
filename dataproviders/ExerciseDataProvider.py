import sqlite3
from sqlite3 import Connection, Cursor

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

    def get_exercises_from_category(self, cat_id: int) -> list:
        """ DEPRECATED Возвращает упражнения из категории по ее id в формате списка словарей """
        columns: list = ["id", "title", "instruction"]
        query: str = f"SELECT { ', '.join(columns) } from exercises where category = { cat_id } order by `order`"
        result = self.cur.execute(query)  #TODO add type
        exercises_data: list = self.cur.fetchall()
        exercises: list = [dict(zip(columns, row)) for row in exercises_data]
        return exercises

    def get_exercise_by_id(self, ex_id: int) -> dict:
        """ DEPRECATED Возвращает полную информацию об упражнении по его id"""

        columns: list = ["id", "title", "instruction", "sql_base", "sql_solution", "tables"]
        query: str = f"SELECT { ', '.join(columns) } from exercises where id = { ex_id } LIMIT 1"
        result = self.cur.execute(query)  # TODO add type
        exercise_data: list = self.cur.fetchone()

        return dict(zip(columns, exercise_data))

    def get_exercise_object(self, ex_id: int) -> Exercise:
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

    def get_exercises_objects_from_category(self, cat_id: int) -> list:

        """ Возвращает упражнения из категории по ее id в формате списка словарей """

        query: str = f"SELECT `id`, `title`, `instruction`" \
                     f"FROM exercises " \
                     f"WHERE category = { cat_id } " \
                     f"ORDER by `order`"

        result: Cursor = self.cur.execute(query)
        exercises_data: list = self.cur.fetchall()
        exercises = [Exercise(*ex) for ex in exercises_data]

        return exercises




