"""URL mappings for recipe app"""

from django.urls import include, path
from recipe import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", views.RecipeViewSet)


app_name = "recipes"

urlpatterns = [path("", include(router.urls))]
