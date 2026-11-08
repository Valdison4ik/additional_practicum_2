from django.http import FileResponse
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import NotFound

from apps.projects.models import ProjectFile
from apps.projects.serializers import CreateProjectFileSerializer, AllProjectFilesSerializer

class ProjectFileViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):

    queryset = ProjectFile.objects.all()
    # serializer_class = CreateProjectFileSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return AllProjectFilesSerializer

        return CreateProjectFileSerializer

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        # 1. Получаем объект из базы данных
        project_file = get_object_or_404(ProjectFile, pk=pk)

        # 2. Открываем файл через встроенное Django-поле
        try:
            file_handle = project_file.data_file.open()
        except FileNotFoundError as e:
            raise NotFound(f"File does not exist:{e}")

        # 3. Возвращаем FileResponse с указанием заголовка скачивания
        response = FileResponse(file_handle, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{project_file.data_file.name}"'
        return response
