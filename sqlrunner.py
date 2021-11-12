import sqlite3

con = sqlite3.connect(':memory:') # Подключаемся к БД
cur = con.cursor() # Запускаем курсор, с помощью которого мы будем получать данные из БД


class SQLRunner:
    def __init__(self):
        pass

    def install_dump(self, query):
        cur.executescript(query) # Выполняем запрос с помощью курсора
        # alldata = cur.fetchall() # С помощью этой функции получаем результат запроса в виде списка кортежей
        # return alldata
        return 0


    def run_query(self, query):
        cur.execute(query) # Выполняем запрос с помощью курсора
        alldata = cur.fetchall() # С помощью этой функции получаем результат запроса в виде списка кортежей
        return alldata


    def run_solution(self):
        pass
