from django.contrib import admin
from apps.projects.models import Project, ProjectFile


@admin.action(description="Заменить пробелы на нижние подчеркивания")
def make_spaces_with_underscores(modeladmin, request, queryset):
    for obj in queryset:
        if obj.name:
            obj.name = obj.name.replace(' ', '_')
            # obj.description = obj.description.replace(' ', '_')
            obj.save()


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'files_number', 'created_at')
    search_fields = ('name',)
    actions = [make_spaces_with_underscores]

    @admin.display(description='Кол-во файлов')
    def files_number(self, obj):
        return obj.files_number


@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'data_file', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
