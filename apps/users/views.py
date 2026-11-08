from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins

from apps.users.models import User
from apps.users.serializers import AllUsersSerializer, RegisterUserSerializer


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
    #             mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = AllUsersSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterUserSerializer
        return self.serializer_class