from django.urls import path
from user.views import AuthTokenView, CreateUserApiView, MangeUserView

app_name = "user"


urlpatterns = [
    path(route="create/", name="create", view=CreateUserApiView.as_view()),
    path(route="token/", name="token", view=AuthTokenView.as_view()),
    path(route="me/", view=MangeUserView.as_view(), name="me"),
]
