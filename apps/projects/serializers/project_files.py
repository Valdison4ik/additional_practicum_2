from typing import Any
from rest_framework.serializers import ModelSerializer, FileField, SlugRelatedField
from apps.projects.models import ProjectFile, Project
from apps.projects.utils import validate_file_size, validate_file_extension
from apps.projects.serializers import ProjectShortInfoSerializer

class AllProjectFilesSerializer(ModelSerializer):
    projects = ProjectShortInfoSerializer(read_only=True, many=True)

    class Meta:
        model = ProjectFile
        fields = ['id','name','projects','data_file','created_at']


class CreateProjectFileSerializer(ModelSerializer):
    # Добавляем валидаторы к полю data_file
    data_file = FileField(validators=[validate_file_size, validate_file_extension],
                          label='Файл')
    projects = SlugRelatedField(many=True
                              ,slug_field='id'
                              , queryset=Project.objects.all()
                              , label='Проекты')

    class Meta:
        model = ProjectFile
        fields = ['id','name','data_file','projects','created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data: dict[str, Any]) -> ProjectFile:
        # организация сохранения связи Многие-ко-Многим
        projects = validated_data.pop('projects', [])
        project_file = ProjectFile.objects.create(**validated_data)
        for project in projects:
            project_file.projects.add(project)
            project_file.save()
        return project_file