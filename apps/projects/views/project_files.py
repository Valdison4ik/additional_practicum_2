from rest_framework import viewsets
from rest_framework import mixins

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
