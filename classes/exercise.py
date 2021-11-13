from sqlrunner import SQLRunner

class Exercise:
    """ Класс, инкапсулирующий всю работу с задачками - выполнение SQL, загрузку итд """

    def __init__(self, topic: str, code: str, sql: str, text: str):

        self.topic: str = topic
        self.code: str = code
        self.sql: str = sql
        self.text: str = text
        self.sql_runner: SQLRunner = SQLRunner()

    def install_dump(self):

        self.sql_runner.install_dump(self.sql)

        return ""

    def run_query(self, query: str) -> list:

        result: list = self.sql_runner.run_query(query)
        return result

    def get_text(self) -> str:
        return self.text

    def get_pretty(self) -> str:
        pretty: str = self.sql_runner.get_prettytable()
        return f"``` \n{pretty} \n```"

