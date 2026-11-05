from django.db import models


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=100, blank=False, null=False, verbose_name="Тег")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        db_table = 'tags'