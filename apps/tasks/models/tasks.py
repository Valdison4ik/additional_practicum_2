from django.db import models
from django.core.validators import MinLengthValidator
# from django.conf import settings
from config import settings
from apps.base.models import TimeStampModel3
from apps.projects.models import Project
from apps.tasks.models.tags import Tag


class Task(TimeStampModel3):
    class Statuses(models.TextChoices):
        NEW = 'new', 'New'
        RUNNING = 'running', 'Running'
        DONE = 'done', 'Done'

    class Priorities(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'middle', 'Middle'
        HIGH= 'high', 'High'
        HIGHEST= 'highest', 'Highest'

    name = models.CharField(unique=True, max_length=100,
                            validators=[MinLengthValidator(10, message="Минимальная длина названия - 10 символов.")],
                            verbose_name="Название задачи")
    # slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True, verbose_name="Описание задачи")
    status = models.CharField(default='new', max_length=15,
                              choices=Statuses,
                              verbose_name="Статус задачи")
    priority = models.CharField(max_length=15, choices=Priorities, verbose_name="Приоритет задачи")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', verbose_name="Проект")
    due_date = models.DateField(blank=True, null=True, verbose_name="Выполнить до")
    assignee = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='tasks',
                                    verbose_name="Исполнитель")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['due_date', 'assignee']
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        constraints = [models.UniqueConstraint(fields=['name', 'project'], name='unique_name_project')]
        db_table = 'tasks'
