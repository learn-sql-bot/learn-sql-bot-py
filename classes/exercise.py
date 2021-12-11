from dataclasses import dataclass


@dataclass
class Exercise:
    """ Информация об упражнении"""

    id: int
    title: str
    instruction: str

    sql_base: str = ""
    sql_solution: str = ""
    sql_tables: str = ""     # строка в которой ранятся таблицы через запятую
    tables: list = ""        # строка в которой ранятся таблицы списком
    pretty: str = ""


