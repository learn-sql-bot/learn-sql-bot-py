import sqlite3
from sqlite3 import Connection

from typing import List

from config import DBPATH
from classes.category import Category


class CategoryDataProvider:
    """ Поставщик данных о категориях """

    def __init__(self, db_path=None):

        if not db_path:
            db_path = DBPATH

        # Подключаемся к БД
        self.connect: Connection = sqlite3.connect(db_path)

        # Запускаем курсор, с помощью которого мы будем получать данные из БД
        self.cur = self.connect.cursor()

    def get_all(self) -> List[Category]:

        """ Возвращает все категории в виде датаклассов """

        sql = f"SELECT id, code, title, `order` " \
              f"FROM categories "

        result = self.cur.execute(sql)
        categories_data = self.cur.fetchall()
        categories = [Category(*cat) for cat in categories_data]
        return categories

    def get_by_id(self, cat_id: int) -> Category:
        """ Возвращает объект категории (в виде датакласса) пол ее ID"""

        sql = f"SELECT id, code, title, `order` " \
              f"FROM categories " \
              f"WHERE id={cat_id}"

        result = self.cur.execute(sql)
        category_data = self.cur.fetchone()

        return Category(*category_data)


