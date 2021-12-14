from classes.exercise import Exercise
from classes.sqlrunner import SQLRunner, SQLRunnerResult
from dataproviders.ExerciseDataProvider import ExerciseDataProvider


class ExerciseService:
    """ Бизнес логика для работы с упражнениями –
        получение упражнения и получения пользовательского решения
        """

    def __init__(self):

        self.sql_runner = SQLRunner()
        self.exercise_data_provider = ExerciseDataProvider()

    def get_exercise_instruction(self, ex_id: int):
        """ Вытаскивает информацию о задании, возвращает данные для отгрузки пользователю
        """
        exercise = self.exercise_data_provider.get_by_id(ex_id)

        # Здесь заводим базу
        sql_base = exercise.sql_base
        self.sql_runner.install_dump(sql_base)

        # Здесь рисуем структуру таблицы
        exercise.pretty = self._get_pretty_tables(exercise)

        return exercise

    def check_user_solution(self, ex_id: int, user_query: str) -> (SQLRunnerResult, SQLRunnerResult):
        """ Проверяет решение пользователя, возвращает два результата запроса
            Внутри каждого - результат, красивая табличка,
        """

        # Заводим базу
        exercise = self.get_exercise_instruction(ex_id)

        # Выполняем запрос
        user_result: SQLRunnerResult = self.sql_runner.run_query(user_query)
        solution_result: SQLRunnerResult = self.sql_runner.run_query(exercise.sql_solution)

        return user_result, solution_result

    def show_example(self, ex_id: int) -> SQLRunnerResult:

        # Заводим базу
        exercise = self.get_exercise_instruction(ex_id)
        solution_result: SQLRunnerResult = self.sql_runner.run_query(exercise.sql_solution)

        return solution_result

    def _get_pretty_tables(self, exercise: Exercise):

        tables = exercise.tables
        query = f"SELECT * from `{ tables[0] }` LIMIT 2"
        result = self.sql_runner.run_query(query)
        return f"Таблица {tables[0]} \n{result.pretty}\n(показаны 2 строки)"
