import pytest

from dataproviders.ExerciseDataProvider import ExerciseDataProvider


class TestExerciseDataProvider:

    def test_exercises_by_category(self):
        exercise_provider = ExerciseDataProvider()
        exercises = exercise_provider.get_exercises_from_category(1)
        assert len(exercises) > 0, "Список зданий существующей категори пустой"
        assert type(exercises) == list, "Список заданий в категории это не список"
        assert type(exercises[0]) == dict, "Первое задание в категории 1 - не словарь"
        assert {"id", "title", "instruction"} == set(exercises[0].keys()), "Список ключей не совпадает"


    def test_exercises_in_nonexistent_category(self):
        exercise_provider = ExerciseDataProvider()
        exercises = exercise_provider.get_exercises_from_category(999)
        assert len(exercises) == 0, "В несуществующей категории есть тест"
