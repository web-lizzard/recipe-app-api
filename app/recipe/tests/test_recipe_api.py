"""Tests for recipe REST API"""

from decimal import Decimal

from core.models import Recipe, Tag, User
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from recipe.serializers import RecipeDetailsSerializer, RecipeSerializer
from rest_framework import status
from rest_framework.test import APIClient

RECIPES_URL = reverse("recipes:recipe-list")


def get_detail_url(recipe_id: str):
    return reverse("recipes:recipe-detail", args=[recipe_id])


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


def create_user(**params):
    """Create and return a new user"""

    return get_user_model().objects.create_user(**params)


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
        self.user: User = create_user(email="test@example.com", password="somepassword")
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
            user=create_user(email="test1@example.com", password="somepasss12")
        )

        response = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_recipe_detail(self):
        """Test get recipe detail"""

        recipe = create_recipe(self.user)
        url = get_detail_url(recipe.id)
        response = self.client.get(url)
        serializer = RecipeDetailsSerializer(recipe)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_recipe(self):
        """Test creating a recipe"""

        payload = {"title": "Sample", "time_minutes": 30, "price": Decimal("3.2")}
        response = self.client.post(RECIPES_URL, payload)
        recipe = Recipe.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, value in payload.items():
            self.assertEqual(getattr(recipe, key), value)
        self.assertEqual(self.user, recipe.user)

    def test_partial_update(self):
        """Test partial update of a recipe"""

        original_link = "https://example.com/recipe.pdf"
        recipe = create_recipe(user=self.user, title="Sample Title", link=original_link)
        payload = {"title": "A New Title"}
        url = get_detail_url(recipe.id)
        response = self.client.patch(url, payload)

        recipe.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.title, payload["title"])
        self.assertEqual(recipe.link, original_link)
        self.assertEqual(recipe.user, self.user)

    def test_full_update(self):
        """Test PUT recipe update"""

        recipe = create_recipe(
            user=self.user,
            title="Recipe Title",
            link="about:blank",
            description="Some description",
        )

        payload = {
            "title": "New recipe",
            "link": "https://example.com",
            "time_minutes": 5,
            "price": Decimal("2.5"),
            "description": "A new description",
        }

        url = get_detail_url(recipe.id)
        response = self.client.put(url, payload)

        recipe.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.user, self.user)

        for key, value in payload.items():
            self.assertEqual(getattr(recipe, key), value)

    def test_update_user_returns_error(self):
        """Test changing a user returns an error"""

        new_user = create_user(email="newuser@example.com", password="somepassword1244")

        payload = {"user": new_user.id}

        recipe = create_recipe(user=self.user)
        url = get_detail_url(recipe.id)
        self.client.patch(url, payload)
        recipe.refresh_from_db()

        self.assertNotEqual(recipe.user, new_user)

    def test_destroy_recipe(self):
        """Test destroy a recipe"""

        recipe = create_recipe(user=self.user)
        url = get_detail_url(recipe.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    def test_create_recipe_with_tags(self):
        """Create recipe with a tags"""

        payload = {
            "title": "Thai Prawn Curry",
            "time_minutes": 30,
            "price": Decimal("4.2"),
            "tags": [{"name": "Thai"}, {"name": "Dinner"}],
        }
        response = self.client.post(RECIPES_URL, payload, format="json")
        recipe = Recipe.objects.get(title=payload["title"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(recipe)
        self.assertEqual(recipe.tags.count(), 2)
        for tag in payload["tags"]:
            is_exists = recipe.tags.filter(user=self.user, name=tag["name"]).exists()

            self.assertTrue(is_exists)

    def test_create_recipe_with_already_existing_tag(self):
        """Test if adding tags to recipe that exists, don't create a duplicate"""

        Tag.objects.create(name="Greek", user=self.user)
        payload = {
            "title": "Salad",
            "time_minutes": 30,
            "price": Decimal("4.2"),
            "tags": [{"name": "Greek"}],
        }
        response = self.client.post(RECIPES_URL, payload, format="json")

        recipe = Recipe.objects.get(title=payload["title"])
        tag = Tag.objects.filter(name="Greek")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(recipe)
        self.assertEqual(recipe.tags.count(), 1)
        self.assertEqual(len(tag), 1)

    def test_update_recipe_with_new_tags(self):
        """Test updating recipe with new tag"""

        recipe = create_recipe(
            self.user, title="Sushi", price=Decimal("2.2"), time_minutes=3
        )
        payload = {"tags": [{"name": "japanese"}]}

        response = self.client.patch(get_detail_url(recipe.id), payload, format="json")
        recipe.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.tags.count(), 1)

        for tag in payload["tags"]:
            is_exists = recipe.tags.filter(user=self.user, name=tag["name"]).exists()

            self.assertTrue(is_exists)

    def test_update_recipe_with_existing_tags(self):
        """Test updating recipe when an existing tag"""

        Tag.objects.create(name="some tag name", user=self.user)
        recipe = create_recipe(
            self.user, title="Some recipe title", price=Decimal("2.2"), time_minutes=3
        )

        payload = {"tags": [{"name": "some tag name"}]}
        response = self.client.patch(get_detail_url(recipe.id), payload, format="json")
        recipe.refresh_from_db()
        tags = Tag.objects.filter(name="some tag name")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(tags.count(), 1)

        for tag in payload["tags"]:
            is_exists = recipe.tags.filter(user=self.user, name=tag["name"]).exists()

            self.assertTrue(is_exists)

    def test_update_clearing_recipe_tags(self):
        """Test if patch new tags to recipe clear previous tags"""

        recipe = create_recipe(
            self.user, title="Breakfast", price=Decimal("2.2"), time_minutes=3
        )
        payload = {"tags": [{"name": "Dinner"}]}

        response = self.client.patch(get_detail_url(recipe.id), payload, format="json")
        recipe.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(recipe.tags.filter(name="Breakfast").exists())
        self.assertTrue(recipe.tags.filter(name="Dinner").exists())
