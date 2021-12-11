from dataprovider import DataProviderLocal

from classes.sqlrunner import SQLRunnerResult


def test_exercise():

    topic: str = "SELECT"
    code: str = "A01"
    data_provider = DataProviderLocal()
    exercise = data_provider.get_exercise_by_topic_and_code(topic, code)
    exercise.install_dump()

    result: SQLRunnerResult = exercise.run_query("SELECT * from user_details")
    print(result)

    pretty_table = exercise.get_pretty()
    print(pretty_table)

def try_query():

    topic: str = "SELECT"
    code: str = "A01"

    data_provider = DataProviderLocal()
    exercise = data_provider.get_exercise_by_topic_and_code(topic, code)
    exercise.install_dump()

    query_1: SQLRunnerResult = exercise.run_query("SELECT * from user_details LIMIT 1")
    if query_1.has_errors(): print("В запросе 1 есть ошибки"); return ""

    query_2: SQLRunnerResult = exercise.run_query("SELECT * from user_details LIMIT 1")
    if query_1.has_errors(): print("В запросе 2 есть ошибки"); return ""

    exercise._compare_results(query_1, query_2)





