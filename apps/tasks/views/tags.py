from rest_framework.request import Request  # для типизации объекта запроса
# from django.http import JsonResponse  # для возврата и типизации ответов
from rest_framework.response import Response
from rest_framework import status  # для указания статусов ответов
from rest_framework.decorators import api_view  # для конкретики обрабатываемых методов

from apps.tasks.serializers.tags import AllTagsSerializer
from apps.tasks.models import Tag


@api_view(['GET', ])
def get_all_tags(request: Request) -> Response:
    all_tags = Tag.objects.all()

    if not all_tags.exists():
        return Response(status=status.HTTP_204_NO_CONTENT)

    serialized_data = AllTagsSerializer(all_tags, many=True)
    return Response(serialized_data.data,
                    status=status.HTTP_200_OK)


@api_view(['GET', ])
def get_tag_by_id(request: Request, tag_id: int) -> Response:
    try:
        tag = Tag.objects.get(id=tag_id)
    except Tag.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)

    serialized_data = AllTagsSerializer(tag)
    return Response(data=serialized_data.data,
                    status=status.HTTP_200_OK)


@api_view(['PUT', ])
def update_required_tag(request: Request, tag_id: int) -> Response:
    try:
        tag = Tag.objects.get(id=tag_id)
    except Tag.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)

    validated_data = AllTagsSerializer(tag, request.data)

    if validated_data.is_valid(raise_exception=True):
        validated_data.save()
        return Response(validated_data.data,
                        status=status.HTTP_200_OK)


@api_view(['POST', ])
def create_tag(request: Request) -> Response:
    new_tag = AllTagsSerializer(data=request.data)

    if new_tag.is_valid(raise_exception=True):
        new_tag.save()
        return Response(new_tag.data,
                        status=status.HTTP_201_CREATED)

    return Response(new_tag.errors,
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
def delete_required_tag(request: Request, tag_id: int) -> Response:
    try:
        tag = Tag.objects.get(id=tag_id)
    except Tag.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)

    tag.delete()
    return Response({'message': f'Tag (id={tag_id}) deleted successfully', },
                    status=status.HTTP_200_OK)
