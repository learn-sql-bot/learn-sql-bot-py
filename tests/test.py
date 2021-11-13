from dataprovider import DataProvider
#
# data = DataProvider.fetch_exercises_by_topic("SELECT")
# print(data)


# data = DataProvider.fetch_exercise_sql_by_topic_and_code("SELECT", "A01")
# print(data)



data = DataProvider.fetch_exercise_text_by_topic_and_code("SELECT", "A01")
print(data)
