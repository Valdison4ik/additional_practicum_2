from django.contrib import admin
from apps.tasks.models import Tag, Task

@admin.action(description="Установить статус Выполнено")
def make_status_done(modeladmin, request, queryset):
    for obj in queryset:
        obj.status = 'done'
        obj.save()


@admin.action(description="Установить приоритет Низкий")
def make_priority_low(modeladmin, request, queryset):
    for obj in queryset:
        obj.priority = 'low'
        obj.save()


@admin.action(description="Установить приоритет Средний")
def make_priority_middle(modeladmin, request, queryset):
    for obj in queryset:
        obj.priority = 'middle'
        obj.save()


@admin.action(description="Установить приоритет Высокий")
def make_priority_high(modeladmin, request, queryset):
    for obj in queryset:
        obj.priority = 'high'
        obj.save()


@admin.action(description="Установить приоритет Очень высокий")
def make_priority_highest(modeladmin, request, queryset):
    for obj in queryset:
        obj.priority = 'highest'
        obj.save()

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'status', 'priority', 'assignee', 'created_at', 'due_date')
    search_fields = ('name',)
    list_filter = ('project', 'status', 'priority', 'assignee', 'created_at', 'due_date')
    actions = [make_priority_highest,
               make_priority_low,
               make_priority_middle,
               make_priority_high,
               make_status_done]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
