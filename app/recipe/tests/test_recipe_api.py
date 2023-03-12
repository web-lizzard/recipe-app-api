"""Tests for recipe REST API"""

from decimal import Decimal

from core.models import Recipe, User
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from recipe.serializers import RecipeSerializer
from rest_framework import status
from rest_framework.test import APIClient

RECIPES_URL = reverse("recipe:recipe-list")


def create_recipe(user: User, **params):
    """Create a sample recipe"""

    defaults = {
        "title": "Sample title",
        "time_minutes": 33,
        "price": Decimal("5.25"),
        "description": "Sample Desc",
        "link": "http://example.come/recipe.pdf",
    }

    defaults.update(params)
    recipe = Recipe.objects.create(user=user, **defaults)

    return recipe


class PublicRecipeAPITests(TestCase):
    """Test unaunthetncitated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""

        response = self.client.get(RECIPES_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user: User = get_user_model().objects.create_user(
            email="test@example.com", password="somepassword"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes"""

        for _ in range(2):
            create_recipe(user=self.user)

        response = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        """Test retrieving a list depends on authentication"""

        create_recipe(user=self.user)
        create_recipe(
            user=get_user_model().objects.create_user(
                email="test1@example.com", password="somepasss12"
            ),
        )

        response = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
