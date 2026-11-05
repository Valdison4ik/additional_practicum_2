from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.request import Request  # для типизации объекта запроса
# from django.http import JsonResponse  # для возврата и типизации ответов
from rest_framework.response import Response
from rest_framework import status  # для указания статусов ответов
from rest_framework.decorators import api_view  # для конкретики обрабатываемых методов
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


from apps.tasks.serializers import (AllTasksSerializer
, TaskInfoSerializer
, CreateUpdateTaskSerializer
, TaskDetailSerializer)
from apps.tasks.models import Task
from apps.base.pagination import BasePagination
from serializers import TaskDetailSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    pagination_class = BasePagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    # filterset_fields = ('project',)

    search_fields = ('project',)
    filterset_fields = ('assignee', 'project',)

    def get_serializer_class(self):
        if self.action in ('create','update','partial_update'):
            return CreateUpdateTaskSerializer
        return TaskDetailSerializer


class TaskListCreateViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = CreateUpdateTaskSerializer
    pagination_class = BasePagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    # filterset_fields = ('project',)

    search_fields = ('project',)
    filterset_fields = ('assignee', 'project',)
    # filterset_fields = {
    #      'project__slug': ['exact'],
    #      'due_date': ['year', 'year__gte', 'year__lte'],
    #  }


class TaskDetailViewSet(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = Task.objects.all()
    # serializer_class = TaskDetailSerializer

    def get_serializer_class(self):
        if self.action == 'update':
            return CreateUpdateTaskSerializer
        return TaskDetailSerializer


@api_view(['GET', ])
def get_all_tasks(request: Request) -> Response:
    project_name = request.query_params.get('project')

    if not project_name:
        all_tasks = Task.objects.all()
    else:
        all_tasks = Task.objects.filter(project__name=project_name)

    if not all_tasks.exists():
        return Response(status=status.HTTP_204_NO_CONTENT)

    serialized_data = AllTasksSerializer(all_tasks, many=True)
    return Response(serialized_data.data,
                    status=status.HTTP_200_OK
                    )


@api_view(['GET', ])
def get_task_by_id(request: Request, task_id: int) -> Response:
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response(data={},
                        status=status.HTTP_204_NO_CONTENT)

    serialized_data = TaskInfoSerializer(task)
    return Response(data=serialized_data.data,
                    status=status.HTTP_200_OK)
