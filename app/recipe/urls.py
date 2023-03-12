"""URL mappings for recipe app"""

from django.urls import include, path
from recipe import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("recipes", views.RecipeViewSet)
router.register("tag", views.TagViewSet)


app_name = "recipes"

urlpatterns = [path("", include(router.urls))]
