from dataproviders.ExerciseDataProvider import ExerciseDataProvider
from classes.sqlrunner import SQLRunner, SQLRunnerResult

class ExerciseService:

    def __init__(self):

        self.sql_runner = SQLRunner()

    def get_exercise_instruction(self, ex_id: int):

        """ Вытаскивает информацию о задании, возвращает данные для отгрузки пользователю"""
        exercise_data_provider = ExerciseDataProvider()
        exercise = exercise_data_provider.get_exercise_by_id(ex_id)

        # Здесь заводим базу

        sql_base = exercise.get("sql_base")
        self.sql_runner.install_dump(sql_base)

        # Здесь рисуем структурку таблицы
        query = "SELECT * from `animals` LIMIT 2"
        result = self.sql_runner.run_query(query)
        exercise['pretty'] = result.pretty

        return exercise

    def check_user_solution(self, ex_id: int, user_query: str) -> (SQLRunnerResult, SQLRunnerResult):
        """ Проверяет решение пользователя, возвращает два результата запроса
            Внутри каждого - результат, красивая табличка,
        """

        # Заводим базу
        exercise = self.get_exercise_instruction(ex_id)

        # Выполняем запрос
        user_result: SQLRunnerResult = self.sql_runner.run_query(user_query)
        solution_result: SQLRunnerResult = self.sql_runner.run_query(exercise.get("sql_solution"))

        return user_result, solution_result



