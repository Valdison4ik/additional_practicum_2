from rest_framework.serializers import ModelSerializer, CharField, ValidationError, DateTimeField
from django.contrib.auth.password_validation import validate_password
import re

from apps.users.models import User



class AllUsersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id',
                  'first_name',
                  'last_name',
                  'position',
                  'email',
                  'phone',
                  'last_login',
                  'created_at']


class RegisterUserSerializer(ModelSerializer):
    re_password = CharField(max_length=128, write_only=True, label='Повтор пароля')

    class Meta:
        model = User
        fields = [
                'username',
                'first_name',
                'last_name',
                'email',
                'position',
                'password',
                're_password'
                ]
        extra_kwargs = {'password': {'write_only': True, 'label':'Пароль'}}

    def validate(self, data):
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        if not re.match('^[a-zA-Z0-9_]*$', username):
            raise ValidationError("The username must be alphanumeric characters or have only _ symbol")

        if not re.match('^[a-zA-Zа-яА-Я-]*$', first_name):
            raise ValidationError("The first name must contain only alphabet symbols")

        if not re.match('^[a-zA-Z-]*$', last_name):
            raise ValidationError("The last name must contain only alphabet symbols")

        password = data.get("password")
        re_password = data.get("re_password")

        if password != re_password:
            raise ValidationError({"password": "Passwords don't match"})

        try:
            validate_password(password)
        except ValidationError as err:
            raise ValidationError({"password": err})

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('re_password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user