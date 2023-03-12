"""Views for the recipe API's """

# Create your views here.

from core.models import Recipe
from recipe.serializers import RecipeSerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class RecipeViewSet(viewsets.ModelViewSet):
    """Viewset for recipe CRUD operations"""

    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieves recipes for authenticated users"""

        return self.queryset.filter(user=self.request.user).order_by("-id")
