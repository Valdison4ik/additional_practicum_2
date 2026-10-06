from django.contrib import admin

from apps.project_manager.models import Project, Tag, Task, ProjectFile


# Register your actions here.

@admin.action(description="Заменить пробелы на нижние подчеркивания")
def make_spaces_with_underscores(modeladmin, request, queryset):
    """
    Задача 13 Additional practicum 2: Django.
    Добавьте возможность заменять пробелы на нижние подчёркивания для объектов проекта. Для этого выполните действия:
    1. Создайте Админ-действие, которое позволит к выделенным объектам применять операцию по замене одного символа на другой.
    2. Дайте этому Админ-действию более понятное название.
    """
    for obj in queryset:
        if obj.name:
            obj.name = obj.name.replace(' ', '_')
            obj.save()


# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Задача 4 Additional practicum 2: Django.
    Необходимо настроить административную панель для удобного отображения и управления моделями.
    Настройте отображение моделей в админ-панели. Реализуйте следующие возможности:
    1. Поиск по названию задачи для модели Task.
    3. У модели Task в Админ-панели должны отображаться поля:
    – Название задачи
    – Проект
    – Статус
    – Приоритетность
    – Дата создания
    – Дата сдачи задачи (due_date)
    5. Для модели Task должна быть возможность фильтрации определённых задач
    по полям:
    – Статус
    – Приоритетность
    – Проект
    – Дата создания
    – Дата сдачи зада

    Задача 6 Additional practicum 2: Django.
    Добавьте нового пользователя и задачи для него. Для этого выполните действия:
    2. Добавьте assignee в список отображаемых полей в Административной панели.
    3. Добавьте в Административную панель возможность фильтрации задач по конкретному assignee.
    """
    list_display = ('name', 'project', 'status', 'priority', 'assignee', 'created_at', 'due_date')
    search_fields = ('name',)
    list_filter = ('project', 'status', 'priority', 'assignee', 'created_at', 'due_date')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Задача 4 Additional practicum 2: Django.
    Необходимо настроить административную панель для удобного отображения и управления моделями.
    Настройте отображение моделей в админ-панели. Реализуйте следующие возможности:
    2. Поиск по названию проекта для модели Project.
    4. У модели Project должны отображаться поля:
    – Название проекта
    – Дата создания проекта

    Задача 12 Additional practicum 2: Django.
    Добавьте отображение количества файлов для каждого проекта. Для этого выполните действия:
    2. Добавьте в Административный класс ProjectAdmin возможность отображения нового поля «count of Files»,
    которое будет содержать кол-во файлов для конкретного проекта.
    3. Добавьте полученную логику в список отображаемых полей.

    Задача 13 Additional practicum 2: Django.
    Добавьте возможность заменять пробелы на нижние подчёркивания для объектов проекта. Для этого выполните действия:
    3. Зарегистрируйте это действие для модели Project в Админ панели.

    """
    list_display = ('name', 'files_number', 'created_at')
    search_fields = ('name',)
    actions = [make_spaces_with_underscores]

    @admin.display(description='Кол-во файлов')
    def files_number(self, obj):
        return obj.files_number


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Настройка отображения тегов в админ-панели со следующими возможностями:
    Поиск по названию тега
    У модели Tag отображаются поля:
    – Название проекта
    """
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    """
    Задача 10 Additional practicum 2: Django.
    Настройте новую модель ProjectFile:
    1. Настройте отображение полей в Административной модели:
    – Имя файла
    – Сам файл
    – Дата создания
    2. Добавьте возможность искать нужный файл по его имени.
    3. Добавьте возможность фильтровать файлы по дате создания.
    """
    list_display = ('name', 'data_file', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)


"""
Задача 13
Добавьте возможность заменять пробелы на нижние подчёркивания для объектов проекта. Для этого выполните действия:
1. Создайте Админ-действие, которое позволит к выделенным объектам применять операцию по замене одного символа на другой.
2. Дайте этому Админ-действию более понятное название.
3. Зарегистрируйте это действие для модели Project в Админ панели.
"""
