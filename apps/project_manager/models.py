from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import User


class TimeStampModel1(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        abstract = True


class TimeStampModel2(TimeStampModel1):
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        abstract = True


class TimeStampModel3(TimeStampModel2):
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name="Дата удаления")

    class Meta:
        abstract = True


# Create your models here.
class ProjectFile(TimeStampModel1):
    """
    Задача 9 Additional practicum 2: Django.
    1. Создайте новую модель ProjectFile для файлов проекта. Модель должна включать поля:
    – Название файла: обязательно к заполнению, максимальная длина имени - 120 символов
    – Файл: должен загружаться в папку «проекты»
    – Дата создания файла: заполняется автоматически только при создании

    Задача 11 Additional practicum 2: Django.
    Настройте дополнительные настройки для модели ProjectFile.
    1. Настройте возможность отображения названия модели во множественном и единственном числах.
    2. Настройте порядок отображения файлов в Административной панели по дате создания
    (от самого последнего созданного файла к самому первому созданному).
    """
    name = models.CharField(max_length=120, blank=False, verbose_name="Имя файла")
    data_file = models.FileField(blank=False, verbose_name="Файл") # upload_to=''

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Файл проекта'
        verbose_name_plural = 'Файлы проектов'

    def __str__(self):
        return self.name


class Project(TimeStampModel1):
    """
    Задача 1 Additional practicum 2: Django.
    Создайте модель Project со следующими полями:
    Название проекта: строковое, уникальное
    Описание проекта: строковое, большое поле, обязательно к заполнению
    Дата создания проекта: должна проставляться автоматически при создании

    Задача 7 Additional practicum 2: Django.
    Добавьте настройки к модели Project:
    1. Добавьте порядок отображения всех проектов по их названию в порядке убывания.
    2. Добавьте отображение названия модели Project во множественном и единственном числах.
    3. Добавьте настройку уникальности каждого проекта сразу по нескольким полям (название и описание проекта).

    Задача 9 Additional practicum 2: Django.
    2. Добавьте новое поле для файлов в модель Project, свяжите его с новой моделью ProjectFile.
    Предполагается, что одни и те же файлы могут быть в разных проектах, каждый проект может иметь много файлов

    Задача 12 Additional practicum 2: Django.
    Добавьте отображение количества файлов для каждого проекта. Для этого выполните действия:
    1. Добавьте property поле для модели Project, которое позволит получать кол-во файлов для конкретного объекта Project.
    2. Добавьте в Административный класс ProjectAdmin возможность отображения нового поля «count of Files»,
    которое будет содержать кол-во файлов для конкретного проекта.
    3. Добавьте полученную логику в список отображаемых полей.
    """

    name = models.CharField(unique=True, max_length=100, verbose_name="Название проекта")
    description = models.TextField(blank=False, null=False, verbose_name="Описание проекта")
    project_files = models.ManyToManyField(ProjectFile, blank=True, related_name='files', verbose_name="Файлы проекта")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        constraints = [models.UniqueConstraint(fields=['name', 'description'], name='unique_name_description')]

    @property
    def files_number(self):
        return self.project_files.count()


class Tag(models.Model):
    """
    Задача 3 Additional practicum 2: Django.
    1. Создайте модель тегов (Tag):
    – Имя тэга (строковое поле, уникальное)
    """
    name = models.CharField(unique=True, max_length=100, blank=False, null=False, verbose_name="Тег")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Task(TimeStampModel3):
    """
    Задача 2 Additional practicum 2: Django.
    Создайте модель Task со следующими полями:
    Название задачи: строковое поле, уникальное, минимальная длина названия 10 символов
    Описание: большое строковое поле, может быть пустым
    Статус: строковое поле максимальной длины в 15 символов, должно быть полем выбора разных статусов. По умолчанию все задачи новые
    Приоритет: строковое поле максимальной длины в 15 символов, должно быть полем выбора разных приоритетов
    Проект: связь с моделью Project, при удалении проекта все задачи должны удаляться
    Дата создания задачи: поле, поддерживающее и дату, и время, заполняется автоматически только при создании
    Дата обновления: поле, поддерживающее и дату, и время, заполняется автоматически всегда
    Дата удаления: поле, в котором может ничего не быть

    Задача 3 Additional practicum 2: Django.
    Расширьте модель Task дополнительным хранением тегов:
    2. Добавьте поле due_date (срок выполнения) в модель Task.
    3. Свяжите модель Задачи с тегами через связь «Многие ко многим», добавив в модель задачи новое поле tags.

    Задача 5 Additional practicum 2: Django.
    Создайте связь модели пользователя (User) с моделью Task.
    Добавьте связь к модели Task через поле assignee, которое будет ссылаться на
    пользователя. При выборе типа связи учтите, что на одной задаче может быть
    одновременно только один сотрудник.

    Задача 8 Additional practicum 2: Django.
    Добавьте настройки к модели Task:
    1. Добавьте отображение названия модели Task во множественном и единственном числах.
    2. Добавьте порядок отображения всех задач по:
    – дате сдачи задачи от самой дальней даты к самой ближайшей;
    – закреплённому за задачей сотруднику;
    3. Добавьте настройку уникальности задачи по её названию и проекту. Это должна быть одна общая категория.
    """
    name = models.CharField(unique=True, max_length=100,
                            validators=[MinLengthValidator(10, message="Минимальная длина названия - 10 символов.")],
                            verbose_name="Название задачи")
    description = models.TextField(blank=True, null=True, verbose_name="Описание задачи")
    status = models.CharField(default='new', max_length=15,
                              choices=[('new', 'New'), ('running', 'Running'), ('done', 'Done')],
                              verbose_name="Статус задачи")
    priority = models.CharField(max_length=15, choices=[('low', 'Low'), ('middle', 'Middle'), ('high', 'High'),
                                                        ('highest', 'Highest')], verbose_name="Приоритет задачи")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', verbose_name="Проект")
    due_date = models.DateField(blank=True, null=True, verbose_name="Выполнить до")
    assignee = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='tasks',
                                    verbose_name="Исполнитель")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['due_date', 'assignee']
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        constraints = [models.UniqueConstraint(fields=['name', 'project'], name='unique_name_project')]


"""
Задание 16 Additional practicum 2: Django.
Создайте группы разрешений:
1. Создайте группу «Manager». Менеджер может:
– Просматривать все группы
– Просматривать все разрешения
– Добавлять новые разрешения
– Добавлять новых пользователей
– Просматривать всех пользователей
– Создавать, изменять, удалять, просматривать все проекты
– Создавать, изменять, удалять, просматривать все файлы проектов
– Добавлять, изменять, просматривать все тэги
– Добавлять, изменять, просматривать все задачи
2. Создайте группу «Client». Клиент может:
– Создавать, изменять, просматривать список всех пользователей
– Создавать, изменять, просматривать список всех проектов
– Создавать, просматривать список всех файлов проектов
– Создавать, изменять, удалять, просматривать список всех тегов
– Создавать, изменять, удалять, просматривать список всех задач
3. Создайте группу «Developer». Разработчик может:
– Добавлять, изменять, удалять, просматривать список пользователей
– Создавать, изменять, удалять, просматривать все проекты
– Создавать, изменять, удалять, просматривать все файлы проектов
– Создавать, изменять, удалять, просматривать все теги
– Создавать, изменять, удалять, просматривать все задачи


Задание 17  Additional practicum 2: Django.
1. Создайте нового пользователя.
2. После создания измените его, добавив ему поле is_staff, чтобы он смог заходить в Административную панель.
3. Добавьте пользователю группу разрешений «Client».
4. Зайдите под пользователем Клиента.
5. Попробуйте выполнить те действия, которые клиенту не должны быть доступны. Например:
– Удалить проект
– Удалить пользователя
– Изменить файл проекта
"""
