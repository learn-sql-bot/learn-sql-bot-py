import sqlite3
from prettytable import from_db_cursor, PrettyTable


class SQLRunner:
    def __init__(self):

        self.connect = sqlite3.connect(':memory:') # Подключаемся к БД
        self.cur = self.connect.cursor()          # Запускаем курсор, с помощью которого мы будем получать данные из БД

    def install_dump(self, query):
        self.cur.executescript(query) # Выполняем запрос с помощью курсора
        # alldata = cur.fetchall() # С помощью этой функции получаем результат запроса в виде списка кортежей
        # return alldata
        return 0

    def run_query(self, query: str, fetch: bool = True) -> list:
        self.cur.execute(query) # Выполняем запрос с помощью курсора
        if fetch:
            all_data: list = self.cur.fetchall() # С помощью этой функции получаем результат запроса в виде списка кортежей
            return all_data


    def get_prettytable(self):

        self.cur.execute("SELECT * from user_details LIMIT 1")
        table: PrettyTable = from_db_cursor(self.cur)
        return str(table)
