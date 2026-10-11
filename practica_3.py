import os
from tokenize import group

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q
from apps.project_manager.models import Tag, Project, ProjectFile, Task


"""
Задание 1
1. Зайдите в Django shell консоль.
2. Импортируйте модель Tag.
3. Создайте объекты тэгов по направлениям:
* Backend
* Frontend
* Q&A
* Design
* DevOPS
4. Сохраните изменения в базу данных.
"""
tags_list = [Tag(name='Backend'), Tag(name='Frontend'), Tag(name='Q&A')
    , Tag(name='Design'), Tag(name='DevOPS')]
for tag in tags_list:
    tag.save()


"""
Задание 2
Создание проектов
1. Импортируйте необходимый(е) классы для работы.
2. Создайте несколько объектов проекта, используя менеджер objects у модели.
3. Убедитесь, что данные были успешно записаны в базу данных.
"""

project_1 = Project(name='Tiger', description='The Tiger is a predator.')
project_1.save()

project_2 = Project.objects.create(name='Condor', description='The Condor is also a predator.')


"""
Задание 3
Добавление файлов к проектам
1. Импортируйте модели Project, ProjectFile
2. Создайте несколько записей файлов для каждого из существующих проектов.
3. Для каждого объекта проекта, созданного ранее, добавьте объекты созданных файлов методом add().
4. Убедитесь, что данные были созданы и сохранены в базу данных.
"""
file_1 = ProjectFile.objects.create(name='tiger_photo', data_file='проекты/prj1.txt')
file_2 = ProjectFile.objects.create(name='condor_history', data_file='проекты/prj1.txt')

project_1.project_files.add(file_1)
project_2.project_files.add(file_2)

"""
Задание 4
Создание пользователей для работы в проекте
1. Импортируйте модель Пользователя (User), которого по умолчанию предлагает Django.
2. Создайте пять разных пользователей:
* Backend
* Frontend
* DevOPS
* Q&A
* Designer
3. Убедитесь, что все они сохранены в базу данных.
"""
user_list = [User(username='Backend', password='456', email='backend.dev@gmail.com'),
             User(username='Frontend', password='456'),
             User(username='DevOPS', password='456'),
             User(username='Q&A', password='456'),
             User(username='Designer', password='456')]

for user in user_list:
    user.save()

user_1 = User.objects.create(username='charlie',
                             password='456',
                             email='charlie@gmail.com',
                             last_name='Третий',
                             first_name='Чарльз Бредфорд',
                             is_staff=False
                             )
"""
Задание 5
Создание задач для проектов
1. Импортируйте модель Task.
2. Для каждого проекта создайте задачи. По одной-две для каждого тега.
3. Для foreignkey полей передаём объекты, которые мы создавали ранее.
4. Убедитесь, что данные были созданы и сохранены в базу данных.
"""
project_3 = Project.objects.create(name='Alligator', description='The alligator is a predator.')

user_2 = User.objects.create(username='david',
                             password='456',
                             email='david@gmail.com',
                             last_name='Иванов',
                             first_name='Давид',
                             is_staff=True
                             )

tag_1 = Tag.objects.create(name='Backend2')

task_1 = Task.objects.create(name='Skin polishing',
                              description='s',
                              priority='high',
                              project=project_3,
                              due_date='2025-10-10',
                              assignee=user_2)

"""
Задание 6
Добавление тэгов для всех задач
1. Получите все объекты тегов.
2. У каждого объекта созданных задач обратитесь к полю тегов через точку.
3. У поля ManyToMany (tags) вызовите метод add и передайте ему объект тега.
* Объект тега будет зависеть от того, какой title будет в задаче, например: (‘Добавить новый эндпоинтʼ - Backend tag, ‘Обновить страницу ответа 404ʼ - Frontend tag)
"""
task_1.tags.add(tag_1)

"""
Задание 7
Получение тегов
1. Импортируйте модели тегов Tag.
2. Напишите запрос, который позволит получить список всех тегов.
3. Выведите имя каждого тега.
4. Получите самый первый тег.
5. Получите самый последний тег.
6. Получите кол-во всех тегов.
"""

all_tags = Tag.objects.all()
for tag in all_tags:
    print(tag.name)

first_tag = Tag.objects.first()
first_tag.name

last_tag = Tag.objects.last()
last_tag.name

count_tag = Tag.objects.count()
count_tag

"""
Задание 8
Проверка существования тега с именем
1. Напишите запрос, который будет искать тэг по определённому имени
2. Проверьте наличие такого тега методом, который выдаёт True или False на наличие объекта.
"""

concret_tag = Tag.objects.filter(name='t5').exists()
concret_tag

"""
Задание 9
Фильтрация тегов по имени
1. Напишите запрос, который позволит получить теги, у которых в имени будет совпадение по
переданной строке, например: “...Tagˮ
2. Выведите имена всех этих тегов.
"""

like_tag = Tag.objects.filter(name__icontains='end')
print(like_tag)

for tag in like_tag:
    print(tag.name)


"""
Задание 10
Фильтрация проектов по дате создания
1. Импортируйте модуль datetime и модель Project.
2. Создайте объект даты, по которой нужно сделать поиск.
3. Напишите запрос, который позволит получить список проектов, которые равны или старше переданной даты создания.
4. Выведите имена таких проектов.
"""

seek_date = timezone.datetime(2026, 10, 7).astimezone()

seek_projects = Project.objects.filter(created_at__gte=seek_date)
for prj in seek_projects:
    print(prj)

"""
Задание 11
Использование Q-класса для комбинированных условий
1. Импортируйте модель Project. 
2. Напишите запрос, который позволит получить необходимые проекты:
* Реализуйте фильтрацию, которая будет проходить два условия:
 - Проекты, равные или больше указанной даты
 - Проекты, у которых в имени есть строка 'TI'
3. Выведите имена таких проектов.
"""
# from django.db.models import Q

q_11_prg = Project.objects.filter(Q(created_at__gte=seek_date) & Q(name__icontains='g'))
q_11_prg
q_11_prg[0].description

"""
Задание 12
Получение списка всех файлов для проекта
1. Напишите запрос, который позволит получить список всех файлов, которые привязаны к конкретному проекту. Поиск произведите по имени проекта.
2. Выведите только пути к каждому файлу.
"""

q_12_01_prg = Project.objects.filter(project_files__name__icontains='FFF')

# q_12_prg = ProjectFile.objects.filter(files__name__contains='world')
q_12_prg = ProjectFile.objects.filter(projects__name__contains='world')
for file in q_12_prg:
    print(file.data_file)


"""
Задание 13
Фильтрация задач по статусу и приоритету
1. Напишите запрос, который поможет получить только те задачи, у которых:
* Статус 'new'
* Приоритетность 'Urgent' Highest
2. Выведите информацию по каждой такой задаче:
* Название
* Статус
* Приоритетность
* Дата, когда задача должна быть сдана
* Email сотрудника, за которым закреплена эта задача
"""

q_13_tsk = Task.objects.filter(status='new', priority='high').select_related()

q_13_tsk

for obj in q_13_tsk:
    print("=" * 50)
    print(obj.name)
    print(obj.status)
    print(obj.priority)
    print(obj.due_date)
    print(obj.assignee.email)
    print("=" * 50)

