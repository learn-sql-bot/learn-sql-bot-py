import pytest

from dataproviders.CategoryDataProvider import CategoryDataProvider


class TestCategoryDataProvider:

    def test_all_categories(self):
        """ Проверяем , что спеисок категорий возвращается верно"""
        category_provider = CategoryDataProvider()
        categories = category_provider.get_categories()
        assert type(categories) == list, "На запрос списка категорий возвращается не список"


    def test_all_categories_not_empty(self):
        category_provider = CategoryDataProvider()
        categories = category_provider.get_categories()
        assert len(categories) > 0, "Список категорий пустой"

    def test_get_category_by_id(self):
        cat_id = 1
        category_provider = CategoryDataProvider()
        category = category_provider.get_category_by_id(cat_id)
        assert type(category) == dict, "На запрос одной категории возвращается категория"
        assert len(category.keys()) > 0, "В данных по категории нет ключей, а зря "

    def test_get_category_by_code(self):
        code = "SELECT"
        category_provider = CategoryDataProvider()
        category = category_provider.get_category_by_code(code)
        assert type(category) == dict, "На запрос одной категории возвращается категория"
        assert len(category.keys()) > 0, "В данных по категории нет ключей, а зря "

