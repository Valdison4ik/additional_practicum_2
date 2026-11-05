from django.db import models
from apps.base.models import TimeStampModel1


class ProjectFile(TimeStampModel1):
    name = models.CharField(max_length=120, blank=False, verbose_name="Имя файла")
    data_file = models.FileField(blank=False, verbose_name="Файл") # upload_to=''
    # file_path

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Файл проекта'
        verbose_name_plural = 'Файлы проектов'
        db_table = 'project_files'

    def __str__(self):
        return self.name