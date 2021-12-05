# from unittest import TestCase
# from services.CategoryService import CategoryService
# from classes.exercise_category import ExerciseCategory
#
#
# class CategoryServiceTest(TestCase):
#
#     def test_all_categories(self):
#         category_service = CategoryService()
#         categories = category_service.all_categories()
#         self.assertEqual(type(categories), dict, "Неверный тип категорий")
#         self.assertGreater(len(categories), 0, "Слишком мало категорий")
#
#
#     def test_single_category(self):
#
#         category_service = CategoryService()
#         cat = category_service.get_category("select")
#         self.assertEqual(type(cat), ExerciseCategory, "Неверный тип - ждали категорию а получили непонятное")
#         self.assertEqual(cat.title,  "SELECT", "Неверное получение имени" )
#         self.assertGreater(len(cat.exercises),  0, "Слишком мало упражнений внутри")
#
#
