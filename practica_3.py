import os
from tokenize import group

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User
from apps.project_manager.models import Tag, Project, ProjectFile


"""
Задание 1
1. Зайдите в Django shell консоль.
2. Импортируйте модель Tag.
3. Создайте объекты тэгов по направлениям:
○ Backend
○ Frontend
○ Q&A
○ Design
○ DevOPS
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
○ Backend
○ Frontend
○ DevOPS
○ Q&A
○ Designer
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
