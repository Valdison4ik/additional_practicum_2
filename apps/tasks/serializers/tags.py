from rest_framework.serializers import ModelSerializer
from apps.tasks.models import Tag


class AllTagsSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class TagsSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']