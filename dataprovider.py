import requests
import json

""" Здесь класс который получает всякую информацию"""


class DataProvider():

    def __init__(self):
        pass

    @staticmethod
    def get_all_tasks(cls):
        json_string = requests.get("https://raw.githubusercontent.com/learn-sql-bot/learn-sql-bot/main/exercises.json")
        exercises_data = json.loads(json_string)
        return exercises_data


