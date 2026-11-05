from datetime import date
from typing import Any

from django.utils import timezone
from rest_framework.serializers import (ModelSerializer
, SlugRelatedField
, ValidationError
, DateField)

from apps.tasks.models import Task, Tag
from apps.tasks.serializers.tags import AllTagsSerializer, TagsSerializer
from apps.projects.serializers import AllProjectsSerializer, ProjectShortInfoSerializer
from apps.projects.models import Project


class AllTasksSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'status', 'priority']


class TaskInfoSerializer(ModelSerializer):
    tags = AllTagsSerializer(many=True)
    project = AllProjectsSerializer()

    class Meta:
        model = Task
        fields = ['id',
                  'name',
                  'description',
                  'status',
                  'priority',
                  'tags',
                  'project',
                  'created_at',
                  'due_date'
                  ]


class CreateUpdateTaskSerializer(ModelSerializer):
    # tags = TagsSerializer(many=True)
    tags = SlugRelatedField(many=True
                            , slug_field='name'
                            , queryset=Tag.objects.all())

    project = SlugRelatedField(slug_field='name'
                               , queryset=Project.objects.all())
    due_date = DateField(default=timezone.now().date(), input_formats=['%Y-%m-%d', 'ISO-8601'], allow_null=True)

    class Meta:
        model = Task
        fields = ['id',
                  'name',
                  'description',
                  'status',
                  'priority',
                  'project',
                  'tags',
                  'assignee',
                  'due_date',
                  'created_at',
                  'updated_at'
                  ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_description(self, value: str) -> str:
        if len(value) < 10:
            raise ValidationError("The description of the task couldn't be less than 50 characters")
        return value.strip().upper()

    def validate_tags(self, value: list[str]) -> list[str]:
        if value and not Tag.objects.filter(name__in=value).exists():
            raise ValidationError("The tags couldn't be found in the database")
        return value

    def validate_due_date(self, value: str) -> date:
        if value and value < timezone.now().date():
            raise ValidationError("The due_date of the task couldn't be in the past")
        return value

    def create(self, validated_data: dict[str, Any]) -> Task:
        # повышение регистра для имени задачи
        title_data = validated_data.pop('name').strip().upper()
        validated_data['name'] = title_data

        # организация сохранения связи Многие-ко-Многим
        tags = validated_data.pop('tags', [])
        task = Task.objects.create(**validated_data)
        for tag in tags:
            task.tags.add(tag)
            task.save()
        return task
        # return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # организация сохранения связи Многие-ко-Многим
        tags = validated_data.pop('tags', [])
        instance = super().update(instance, validated_data)

        if tags is not None:
            instance.tags.set(tags)

        return instance


class TaskDetailSerializer(ModelSerializer):
    tags = TagsSerializer(many=True, read_only=True)
    project = ProjectShortInfoSerializer()

    class Meta:
        model = Task
        # fields = ['id',
        #           'name',
        #           'description',
        #           'status',
        #           'priority',
        #           'project',
        #           'tags',
        #           'assignee',
        #           'due_date',
        #           'created_at'
        #           ]
        exclude = ('updated_at', 'deleted_at')
