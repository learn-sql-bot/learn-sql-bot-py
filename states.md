### (No state)

Вывести привет, выбери тему для задачек
Переключитьсђна стейт "выбор темы"

### State: select_topic

Принять сообщение если такая тема есть
    Запомнить тему в стейт машине
    Вывестит список задачек в теме 
    Переключиться на стейт "выбор задания"
Иначе
    Вывести сообщение что такой темы нет, попробуйте снова, остаться в стейте
    
### State: select_exercise

Принять сообщение если такая задачка есть
    Запомнить задачку в стейт машине
    Вывести текст задачки
    Переключиться на стейт "решение задания"
Иначе
    Вывести сообщение что такой задачки нет, попробуйте снова, остаться в стейте

### State: solve_exercise

Принять сообщение , записать в строку
Импортнуть БД, выполнить строку как SQL запрос
Получить данные , сверить с образцом

Если совпадает с образцом
    Вывести сообщение "Ура, все верно, давайте решим еще"
    Переключиться на стейт выбор темы - "select_topic"

Если нет совпадения
    Вывести сообщение "Неа, попробуйте снова. /exit для выхода"
    Остаться в стейте