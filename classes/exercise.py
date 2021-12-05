from classes.sqlrunner import SQLRunner, SQLRunnerResult

class Exercise:
    """ Класс, инкапсулирующий всю работу с задачками - выполнение SQL, загрузку итд """

    def __init__(self, topic: str, code: str, sql: str, text: str, solution: str):

        self.topic: str = topic
        self.code: str = code
        self.sql: str = sql
        self.text: str = text
        self.solution: str = solution
        self.sql_runner: SQLRunner = SQLRunner()

    def get_text(self) -> str:
        return self.text

    def get_pretty(self) -> str:
        pretty: str = self.sql_runner.get_prettytable()
        return f"``` \n{pretty} \n```"

    def install_dump(self):
        self.sql_runner.install_dump(self.sql)
        return ""

    def run_query(self, query: str) -> SQLRunnerResult:

        result: SQLRunnerResult = self.sql_runner.run_query(query)
        return result

    ####### COMPARE RESULTS #######

    def _compare_results(self, r1: SQLRunnerResult, r2: SQLRunnerResult):

        if set(r1.columns) == set(r2.columns):
            print("Названия столбцов совпадают")

        if len(r1.rows) == len(r2.rows):
            print("Количество строк совпадает")

    def _compare_results_titles(self, r1: SQLRunnerResult, r2: SQLRunnerResult):
        if set(r1.columns) == set(r2.columns):
            return True
        return False

    def _compare_results_counts(self, r1: SQLRunnerResult, r2: SQLRunnerResult):
        if len(r1.rows) == len(r2.rows):
            return True
        return False



    def get_result(self) -> list:

        results: list = self.sql_runner.fetch()
        return  results
