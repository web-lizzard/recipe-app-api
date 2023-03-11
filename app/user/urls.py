from django.urls import path
from user.views import AuthTokenView, CreateUserApiView

app_name = "user"


urlpatterns = [
    path(route="create/", name="create", view=CreateUserApiView.as_view()),
    path(route="token/", name="token", view=AuthTokenView.as_view()),
]
