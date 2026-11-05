from datetime import datetime
# from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.request import Request # для типизации объекта запроса
# from django.http import JsonResponse # для возврата и типизации ответов
from rest_framework.response import Response
from rest_framework import status # для указания статусов ответов
# from rest_framework.decorators import api_view # для конкретики обрабатываемых методов
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from django.db.models import ProtectedError
from django.utils import timezone

import serializers
from apps.projects.serializers import (AllProjectsSerializer
, CreateProjectSerializer
, DetailProjectSerializer)
from apps.projects.models import Project

"""
@api_view(['GET',])
def get_all_projects(request: Request) -> Response:
    all_projects = Project.objects.all()
    if not all_projects.exists():
        return Response(status=status.HTTP_204_NO_CONTENT)

    serialized_data = CreateProjectSerializer(all_projects, many=True)
    return Response(serialized_data.data,
                    status=status.HTTP_200_OK)
"""

class ProjectDetailViewSet(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    queryset = Project.objects.all()
    serializer_class = DetailProjectSerializer


class ProjectListCreateView(APIView):
    def get_objects(self, date_from=None, date_to=None):
        if date_from:
            date_from = timezone.make_aware(datetime.strptime(date_from, '%Y-%m-%d'))
            projects = Project.objects.filter(created_at__gte=date_from)
        else:
            projects = Project.objects.all()

        if date_to:
            date_to = timezone.make_aware(datetime.strptime(date_to, '%Y-%m-%d'))
            projects = projects.filter(created_at__lte=date_to)

        return projects


    def get(self, request: Request) -> Response:
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        all_projects = self.get_objects(date_from, date_to)

        serializer = AllProjectsSerializer(all_projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = CreateProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProjectDetailView(APIView):

    def get(self, request: Request, project_id: int) -> Response:
        project = get_object_or_404(Project, pk=project_id)
        serializer = DetailProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, project_id: int) -> Response:
        project = get_object_or_404(Project, pk=project_id)
        serializer = CreateProjectSerializer(instance=project
                                             ,data=request.data
                                             ,partial=True
                                             )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, project_id: int) -> Response:
        project = get_object_or_404(Project, pk=project_id)

        # try:
        project.delete()
        """
        except ProtectedError:
            return Response(
                {
                    "Detail": "This book cannot be deleted."
                },
                status=status.HTTP_409_CONFLICT
            )"""

        return Response(status=status.HTTP_204_NO_CONTENT)