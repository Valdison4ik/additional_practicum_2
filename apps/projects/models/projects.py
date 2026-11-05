from django.db import models
from apps.base.models import TimeStampModel1
from .project_files import ProjectFile


class Project(TimeStampModel1):
    name = models.CharField(unique=True, max_length=100, verbose_name="Название проекта")
    description = models.TextField(blank=False, null=False, verbose_name="Описание проекта")
    project_files = models.ManyToManyField(ProjectFile, blank=True, related_name='projects', verbose_name="Файлы проекта")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        constraints = [models.UniqueConstraint(fields=['name', 'description'], name='unique_name_description')]
        db_table = 'projects'

    @property
    def files_number(self):
        return self.project_files.count()
