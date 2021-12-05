import sqlite3
from sqlite3 import Connection, OperationalError
from prettytable import PrettyTable
from dataclasses import dataclass


@dataclass
class SQLRunnerResult:
    executed: bool
    rows: list = None
    columns: list = None
    errors: list = None
    pretty: str = ""


    def has_errors(self) -> bool:
        return len(self.errors) > 0


class SQLRunner:

    def __init__(self):

        self.connect: Connection = sqlite3.connect(':memory:')  # Подключаемся к БД
        self.cur = self.connect.cursor()          # Запускаем курсор, с помощью которого мы будем получать данные из БД
        self.query_result: SQLRunnerResult = SQLRunnerResult(False)

    def install_dump(self, query):
        """ Загружает дамп из файла в базу чтобы использовать в упражнении"""
        result = self.cur.executescript(query) # Выполняем запрос с помощью курсора
        return result

    def run_query(self, query: str) -> SQLRunnerResult:
        """Возвращает результаты запроса в специальном виде с указанием строк и столбцов"""

        try:
            self.cur.execute(query)    # Выполняем запрос с помощью курсора
        except OperationalError as e:

            self.query_result: SQLRunnerResult = SQLRunnerResult(executed=True, errors=[e])
            return self.query_result

        # Получаем колонки
        columns = []
        columns_raw = self.cur.description  # TODO: rewrite to list comps
        for name in columns_raw:
            columns.append(name[0])

        # Получаем строки
        rows = self.cur.fetchall()

        # Запихиваем это все в датакласс
        self.query_result: SQLRunnerResult = SQLRunnerResult(
            rows=rows, columns=columns, executed=True, errors=[]
        )

        # Билдим преттитейбл
        self.get_prettytable()

        # Отдаем готовый датакласс
        return self.query_result

    def get_prettytable(self) -> str:
        """ Рисует красивую аски-табличку, данные берет из объекта ответа"""

        result: SQLRunnerResult = self.query_result
        table: PrettyTable = PrettyTable()
        table.field_names = result.columns

        for row in result.rows:
            table.add_row(row)

        pretty = str(table)

        self.query_result.pretty = pretty

        return pretty




