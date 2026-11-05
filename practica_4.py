import os
import logging
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

sql_logger = logging.getLogger('django.db.backends')
sql_logger.setLevel(logging.DEBUG)
sql_logger.addHandler(logging.StreamHandler())


from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q, F, Count, Avg, Min, Max, Sum
from django.db.models.functions import ExtractWeekDay
from apps.project_manager.models import Tag, Project, ProjectFile, Task


"""
Задание 1
Проекты за текущий месяц
1. Импортируйте модель Project.
2. Импортируйте модуль timezone из django.
3. Напишите запрос, который выдаст только те проекты, которые были созданы в текущем
месяце (месяц брать от даты текущего дня).
4. Если есть хоть один проект - выведите информацию:
○ Название проекта
○ Полная дата его создания
"""

# prj_to_update = Project.objects.filter(name='Linux')
# prj_to_update.update(created_at=F('created_at') - timedelta(days=365))

# cur_month_projects = Project.objects.filter(created_at__year=timezone.now().year,
#                                             created_at__month=timezone.now().month)
#
# if cur_month_projects:
#     for proj in cur_month_projects:
#         print("=" * 50)
#         print(proj.name)
#         print(proj.created_at)
# else:
#     print("EMPTY DATA")

"""
Задание 2
Файлы проектов в день недели
1. Импортируйте модель ProjectFile.
2. Импортируйте класс ExtractWeekDay из django.
3. Напишите запрос, который будет получать список файлов за определённый день, например понедельник:
○ Для выборки конкретного значения по полю даты создания используйте класс ExtractWeekDay.
○ Для упрощения работы с таким значением задайте для него новое, не заявленное в модели поле, например weekday.
○ Проведите фильтрацию по этому новому полю.
4. Если файлов не было найдено - выведите сообщение “Empty Dataˮ, если был найден хоть один файл -
выведите информацию о нём:
○ Название файла
○ Путь к файлу, где он сохранён
"""
#
# monday_project_files = (ProjectFile.objects.annotate(weekday=ExtractWeekDay('created_at')).
#                         filter(weekday=3))
#
# if monday_project_files:
#     for file_ in monday_project_files:
#         print("=" * 50)
#         print(file_.name)
#         print(file_.data_file)
# else:
#     print("EMPTY DATA")

"""
Задание 3
Общее количество проектов
1. Импортируйте модель Project.
2. Напишите запрос, который будет считать количество всех проектов, которые есть в базе данных.
3. Выведите количество всех проектов в консоль.
"""

# cnt = Project.objects.aggregate(total_cnt=Count('id'))
# print(cnt['total_cnt'])
#
# count_of_projects = Project.objects.all().count()
# print(f"Count of projects: {count_of_projects}")

"""
Задание 4
Количество файлов для каждого проекта
1. Импортируйте модель Project.
2. Импортируйте класс Count из django.
3. Напишите запрос, который будет считать количество файлов для каждого проекта персонально.
4. Выведите информацию о количестве файлов для каждого проекта.
"""
#
# cnt_of_files = Project.objects.values('name').annotate(total_files=Count('project_files')).order_by('name')
#
# print(cnt_of_files)

#
# projects = Project.objects.all()
# project_file_counts = {}
#
# for project in projects:
#     file_count = project.project_files.aggregate(num_files=Count('id'))
#     project_file_counts[project.name] = file_count['num_files']
#
# for project_name, num_files in project_file_counts.items():
#     print(f"Project: {project_name}, Number of files: {num_files}")

"""
Задание 5
Среднее количество задач на каждом проекте
1. Импортируйте модель Project.
2. Импортируйте класс AVG из django.
3. Напишите запрос, который сможет для каждого проекта выведите среднее количество задач.
4. Выведите полученные данные.
"""

# avg_task_count = (Project.objects.values('name')
#                   .annotate(task_cnt = Count('tasks'))
#                   .aggregate(Avg('task_cnt'), Min('task_cnt'), Max('task_cnt'), Count('task_cnt'), Sum('task_cnt')))
# print(avg_task_count)


# Мурня полная
# average_project_tasks = Project.objects.annotate(avg_tasks=Avg('tasks__id'))
# # print(average_project_tasks)
# for project in average_project_tasks:
#     print(f"Project: {project.name}, Average Number of Tasks: {project.avg_tasks}")

"""
Задание 6
Количество задач для каждого пользователя
1. Импортируйте модель User из django.
2. Импортируйте класс Count из django.
3. Напишите запрос, который получит из базы данных количество задач для каждого пользователя.
4. В запросе укажите, что хотим работать только с конкретными полями:
○ Username
○ Наше собственно созданное поле count_of_tasks
5. Выведите как результат никнейм разработчика и количество прикреплённых за ним задач.
"""
# (0.001) SELECT "auth_user"."username" AS "username", COUNT("project_manager_task"."id") AS "count_of_tasks" FROM "auth_user" LEFT OUTER JOIN "project_manager_task" ON ("auth_user"."id" = "project_manager_task"."assignee_id") GROUP BY 1 ORDER BY 2 DESC; args=(); alias=default
# user_count = User.objects.values('username').annotate(count_of_tasks=Count('tasks__id')).order_by('-count_of_tasks')
# for user in user_count:
#     print(user['username'], user['count_of_tasks'])


# print('*' * 50)
# (0.000) SELECT "auth_user"."username" AS "username", COUNT("project_manager_task"."id") AS "count_of_tasks" FROM "auth_user" LEFT OUTER JOIN "project_manager_task" ON ("auth_user"."id" = "project_manager_task"."assignee_id") GROUP BY "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", 1, "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined"; args=(); alias=default
# count_of_tasks_to_user = (User.objects.annotate(count_of_tasks=Count('tasks__id'))
#                           .values_list('username','count_of_tasks'))
# print(count_of_tasks_to_user.query)
# for username, count_of_tasks in count_of_tasks_to_user:
#     print(f"Developer - {username} | Count of tasks: {count_of_tasks}")

"""
Задание 7
Сортировка задач по приоритету и дате выполнения
1. Импортируйте модель Task.
2. Напишите запрос, который сможет отсортировать все задачи по нескольким полям:
○ Приоритет задачи
○ Дата к которой задача должна быть выполнена
3. Выведите название задачи, приоритет и дату завершения.
"""

# ordered_tasks = Task.objects.all().order_by('-priority','due_date')
# print(ordered_tasks)
#
# for task in ordered_tasks:
#     print(task.name, task.priority, task.due_date)


# v2
# all_tasks = (Task.objects.order_by('priority','due_date')
#              .values_list('name', 'priority', 'due_date'))
# for name, priority, due_date in all_tasks:
#     print(f"Task name - {name} | Priority: {priority} | Due date - {due_date}")

"""
Задание 8
Сортировка пользователей по количеству задач
1. Импортируйте модель User из django.
2. Напишите запрос, который будет сортировать всех пользователей исходя из того, как много у каждого задач.
3. Отсортируйте от самого загруженного сотрудника, к самому свободному по задачам.
4. Конкретизируйте запрос таким образом, чтобы в него включались только поля:
○ Username
○ Count_of_tasks
5. Выведите все данные в консоль.
"""
# user_count = User.objects.values('username').annotate(count_of_tasks=Count('tasks__id')).order_by('-count_of_tasks')
# for user in user_count:
#     print(user['username'], user['count_of_tasks'])


"""
Задание 9
Пагинация для задач
1. Импортируйте модель Task.
2. Импортируйте класс Paginator.
3. Напишите запрос для получения всех задач.
4. Реализуйте пагинацию для того, чтобы в рамках одной страницы отображалось ровно 10 задач,
не более.
5. Выведите данные об этих 10-ти задачах:
○ Название
○ Статус
○ Приоритетность
○ Username разработчика
"""


# Так делать не надо

# from management_app.models import Task
# from django.core.paginator import Paginator
# tasks = Task.objects.all()
# pages_paginator = Paginator(tasks, 10)
# page_number = 1
# page_tasks = pages_paginator.get_page(page_number)
# for task in page_tasks:
#     print("=" * 50)
#     print(task.name)
#     print(task.status)
#     print(task.priority)
#     print(task.assignee.username)

"""
practica_4
Задание 10
Первый сериализатор для проектов
1. Установите модуль djangorestframework.
2. Добавить этот модуль в файл requirements.txt.
3. Добавить этот модуль в список установленных приложений в файле settings.py.
4. Создать новый пакет serializers, в котором создать первый файл - projects
5. Импортируйте класс ModelSerializer.
6. Напишите первый сериализатор, который будет обрабатывать поля id и name для проекта, выдавая общую базу для вывода всех проектов.
"""

"""
Задание 11
Первое представление для отображения списка всех проектов
1. Импортируйте ранее написанный сериализатор в файл, где будет реализовываться первое
представление.
2. Импортируйте дополнительные методы и классы:
○ Request из rest_framework (для типизации объекта запроса)
○ JsonResponse из django (для возврата и типизации ответов)
○ Status из rest_framework (для указания статусов ответов)
○ Api_view из rest_framework.decorators (для конкретики обрабатываемых методов)
○ Модель Project (для запросов к таблице проектов в базе данных)
3. Напишите функцию, которая будет обрабатывать GET запросы для получения списка всех проектов
из Базы данных.
4. Зарегистрировать эту функцию в списке эндпоинтов в файле urls.py
5. Проверьте работу готового эндпоинта.
"""

# http://127.0.0.1:8000/projects/

"""
Задание 12
Сериализатор для модели задач (Task)
1. Создайте новый файл для сериализаторов задач.
2. Импортируйте класс ModelSerializer.
3. Напишите сериализатор для модели Task с полями id, name, status, priority для получения общей
информации о задачах.
"""

"""
Задание 13
Отображение для получения списка всех задач
1. Импортируйте модель Task
2. Импортируйте написанный ранее сериализатор AllTasksSerializer
3. Напишите отображение, которое будет выводить JSON данные о всех задачах из базы данных:
○ Если при отправке запроса не передавать конкретный проект - выводить все задачи
○ Если был указан конкретный проект, например “TIGERˮ - выводить только те задачи, которые
принадлежат этому проекту
"""

"""
Задание 14
Сериализатор на получение всех тегов
1. Создайте новый файл tags для хранение сериализаторов.
2. Импортируйте класс ModelSerializer.
3. Напишите сериализатор для получения всех тегов.
"""

"""
Задание 15
Отображение для получения всех тегов
1. Импортируйте модель Tag.
2. Импортируйте сериализатор AllTagsSerializer.
3. Напишите функцию, которая будет отображать список всех тегов в формате JSON.
"""

"""
Задание 16
Отображение для получения тега по id 
1. Напишите отображение с принимаемым аргументом tag_id.
2. Проверьте существование такого тега и если он есть - вернуть информацию о нём.
"""

"""
Задание 17
Отображение для обновления информации о теге
1. Поставьте в декоратор api_view() метод для обновления ‘PUTʼ.
2. Напишите запрос, который будет получать конкретный тег по id:
○ Реализуйте проверку на получение объекта тега. Если объекта нет - выведите соответствующее сообщение.
3. Напишите отображение, которое будет принимать из тела запроса новые данные:
○ Реализуйте проверку валидации полученных данных.
4. Обновите полученный объект тега новыми данными и сохраните его.
"""

"""
Задание 18
Представление для создания тега
1. Поставьте в декоратор api_view() метод для обновления ‘POSTʼ.
2. Напишите отображение, которое будет создавать новый объект тега.
○ Реализуйте проверку валидации полученных данных.
3. Сохраните новый объект в базе данных.
"""

"""
Задание 19
Представление для удаления тега
1. Поставьте в декоратор api_view() метод для обновления ‘DELETEʼ.
2. Напишите запрос, который будет получать конкретный тег по id.
3. Напишите отображение, которое будет удалять полученный объект тега и выводить сообщение об
успешном удалении.
"""

"""
Задание 20
Подробная информация о задаче
1. Напишите сериализатор TaskInfoSerializer для получения подробной информации о задаче.
2. Поле для тегов должно быть вложенным объектом, которым является уже готовый сериализатор TagsSerializer.
"""


"""
Задание 21
1. Импортируйте сериализатор TaskInfoSerializer.
2. Напишите функцию с аргументом task_id для получения детальной информации о задаче:
○ Проверьте существование задачи по её id. Если задачи нет - выведите соответствующее
сообщение, если задача есть - выведите её содержимое.
"""