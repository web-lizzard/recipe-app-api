from rest_framework import authentication, generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import CreateTokenSerializer, UserSerializer


class CreateUserApiView(generics.CreateAPIView):
    serializer_class = UserSerializer


class AuthTokenView(ObtainAuthToken):
    serializer_class = CreateTokenSerializer
    renderer_class = api_settings.DEFAULT_RENDERER_CLASSES


class MangeUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
