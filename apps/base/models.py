from django.db import models


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
