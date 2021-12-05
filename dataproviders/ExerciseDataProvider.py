import sqlite3
from sqlite3 import Connection
from config import DBPATH


class ExerciseDataProvider:
    """ Поставщик данных об упражнениях """

    def __init__(self):

        # Подключаемся к БД
        self.connect: Connection = sqlite3.connect(DBPATH)

        # Запускаем курсор, с помощью которого мы будем получать данные из БД
        self.cur = self.connect.cursor()

    def get_exercises_from_category(self, cat_id: int) -> list:
        """ Возвращает упражнения из категории по ее id в формате списка словарей """
        columns: list = ["id", "title", "instruction"]
        query: str = f"SELECT { ', '.join(columns) } from exercises where category = { cat_id } order by `order`"
        result = self.cur.execute(query)  #TODO add type
        exercises_data: list = self.cur.fetchall()
        exercises: list = [dict(zip(columns, row)) for row in exercises_data]
        return exercises

    def get_exercise_by_id(self, ex_id: int) -> dict:
        """ Возвращает полную информацию об упражнении по его id"""

        columns: list = ["id", "title", "instruction", "sql_base", "sql_solution", "tables"]
        query: str = f"SELECT { ', '.join(columns) } from exercises where id = { ex_id } LIMIT 1"
        result = self.cur.execute(query)  # TODO add type
        exercise_data: list = self.cur.fetchone()
        return dict(zip(columns, exercise_data))



