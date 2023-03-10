from rest_framework import generics
from user.serializers import CreateUserSerializer


class CreatUserApiView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
