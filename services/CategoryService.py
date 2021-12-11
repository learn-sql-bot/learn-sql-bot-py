from typing import List

from classes.category import Category
from dataproviders.CategoryDataProvider import CategoryDataProvider
from dataproviders.ExerciseDataProvider import ExerciseDataProvider


class CategoryService:
    """ Бизнес логика для работы с категориями –
        получение всех, одной или какого-то специального набора
        """

    def __init__(self):

        self.category_provider = CategoryDataProvider()
        self.exercise_provider = ExerciseDataProvider()

    def all_categories(self) -> List[Category]:
        """ Возвращает список категорий """
        categories = self.category_provider.get_all()
        return categories

    def get_category(self, cat_id: int) -> Category:
        """ Возвращает одну категорию со списком упражнений"""

        category = self.category_provider.get_by_id(cat_id)
        exercises = self.exercise_provider.get_exercises_objects_from_category(cat_id)
        category.exercises = exercises

        return category


