from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, ValidationError, DateTimeField
from apps.projects.models import Project
from apps.base.models import TimeStampModel1


class AllProjectsSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at']


class CreateProjectSerializer(ModelSerializer):
    # created_at = TimeStampModel1() # read_only=True
    created_at = DateTimeField(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at']

    def validate_description(self, value: str) -> str:
        if len(value) < 15:
            raise ValidationError('Description must be at least 15 characters long')
        return value


class DetailProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ('name', 'description', 'created_at', 'files_number')


class ProjectShortInfoSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name')
