from django.urls import path
from user.views import CreatUserApiView

app_name = "user"


urlpatterns = [path(route="create/", name="create", view=CreatUserApiView.as_view())]
