from dataproviders.CategoryDataProvider import CategoryDataProvider
from dataproviders.ExerciseDataProvider import ExerciseDataProvider


class CategoryService:
    """ Бизнес логика для работы с категориями –
        получение всех, одной или какого-то специального набора
        """

    def __init__(self):
        pass

    def all_categories(self) -> list:
        """ Возвращает список категорий """
        category_provider = CategoryDataProvider()
        categories = category_provider.get_categories()
        return categories

    def get_category(self, cat_id: int) -> dict:
        """ Возвращает одну категорию со списком упражнений"""
        category_provider = CategoryDataProvider()
        exercise_provider = ExerciseDataProvider()

        category = category_provider.get_category_by_id(cat_id)
        exercises = exercise_provider.get_exercises_from_category(cat_id)

        category['exercises'] = exercises
        return category


