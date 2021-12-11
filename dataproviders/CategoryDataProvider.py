import sqlite3
from sqlite3 import Connection

from config import DBPATH


class CategoryDataProvider:
    """ Поставщик данных о категориях """

    def __init__(self):

        # Подключаемся к БД
        self.connect: Connection = sqlite3.connect(DBPATH)

        # Запускаем курсор, с помощью которого мы будем получать данные из БД
        self.cur = self.connect.cursor()

    def get_categories(self) -> list:
        """Получает все категории, сортирует по порядку, отдает в формте списка словарей с ключами id, code, title"""

        columns: list = ["id", "code", "title"]
        sql: str = f"SELECT { ','.join(columns)}  from categories order by `order`"
        result = self.cur.execute(sql)
        category: list = [dict(zip(columns, row)) for row in self.cur.fetchall()]
        return category

    def get_category_by_id(self, cat_id: int) -> dict:

        # Колонки, которые нам понадобятся
        column_names = ["id", "code", "title"]

        # Запрос, который получит колонки
        sql = f"select { ', '.join(column_names) } from categories where id={cat_id}"
        result = self.cur.execute(sql)
        # Получаем одну строчку из ответа
        category_data = self.cur.fetchone()

        # Возвращаем вместо кортежа словарь
        return dict(zip(column_names, category_data))

    def get_category_by_code(self, code: str) -> dict:

        # Колонки, которые нам понадобятся
        column_names = ["id", "code", "title"]

        # Запрос, который получит колонки
        sql = f"select { ', '.join(column_names) } from categories where code='{code}'"
        result = self.cur.execute(sql)
        # Получаем одну строчку из ответа
        category_data = self.cur.fetchone()

        # Возвращаем вместо кортежа словарь
        return dict(zip(column_names, category_data))
