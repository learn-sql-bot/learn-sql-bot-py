# from json import JSONDecodeError
# from typing import IO
#
# import requests
# import json
# from config import TOPICS_URL, BASE_URL
#
# from classes.exercise import Exercise
#
#
# class DataProvider:
#     """ Здесь класс который получает данные, пока из гитхаб репозитория"""
#
#
#     @staticmethod
#     def fetch_topics() -> dict:
#         url = TOPICS_URL
#         try:
#             result = requests.get(url)
#         except Exception:
#             return False
#
#         if result.status_code != 200:
#             return False
#
#         topics_json: str = result.text
#
#         try:
#             topics = json.loads(topics_json.strip())
#         except JSONDecodeError:
#             return False
#         return topics
#
#
#     @staticmethod
#     def fetch_exercises_by_topic(topicname) -> dict:
#         url = f"{BASE_URL}/topics/{topicname}.json"
#         try:
#             exercises_json: str = requests.get(url).text
#         except (requests.ConnectTimeout, requests.HTTPError, requests.ReadTimeout, requests.Timeout, requests.ConnectionError):
#             print("error requesting {url}")
#             return False
#         exercises: list = json.loads(exercises_json.strip())
#         return exercises
#
#
#     @staticmethod
#     def fetch_exercise_sql_by_topic_and_code(topic_name: str, exercise_code: str) -> str:
#         url = f"{BASE_URL}/exercises/{topic_name}/{exercise_code}/data.sql"
#         try:
#             result = requests.get(url)
#         except Exception:
#             return False
#         if result.status_code != 200:
#             return False
#
#         return result.text
#
#     @staticmethod
#     def fetch_exercise_text_by_topic_and_code(topic_name: str, exercise_code: str) -> str:
#         url = f"{BASE_URL}/exercises/{topic_name}/{exercise_code}/task.md"
#         try:
#             result = requests.get(url)
#         except Exception:
#             return False
#         if result.status_code != 200:
#             return False
#
#         return result.text
#
#
# class DataProviderLocal(DataProvider):
#
#
#     def _get_sql_from_file(self, topic: str, code: str) -> str:
#
#         sql_path: str = f"content/{topic}/{code}/data.sql"
#         sql_file = open(sql_path)
#         return sql_file.read()
#
#     def _get_text_from_file(self, topic: str, code: str) -> str:
#
#         task_path: str = f"content/{topic}/{code}/task.md"
#         task_file: IO = open(task_path)
#         task_md: str = task_file.read()
#         return task_md
#
#     def _get_solution_from_file(self, topic: str, code: str) -> str:
#
#         solution_path: str = f"content/{topic}/{code}/solution.sql"
#         solution_file: IO = open(solution_path)
#         solution: str = solution_file.read()
#         return solution
#
#     def get_exercise_by_topic_and_code(self, topic: str, code: str) -> Exercise:
#
#         sql: str = self._get_sql_from_file(topic, code)
#         text: str = self._get_text_from_file(topic, code)
#         solution: str = self._get_solution_from_file(topic, code)
#
#         exercise: Exercise = Exercise(topic=topic, code=code, sql=sql, text=text, solution=solution)
#
#         return exercise
#
#
#
#
#
#
#
#
