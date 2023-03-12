from core.models import Tag
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from recipe.serializers import TagSerializer
from rest_framework import status
from rest_framework.test import APIClient

TAGS_API_URL = reverse("recipes:tag-list")


def get_tag_url(tag_id: str):
    """Return tag url"""
    return reverse("recipes:tag-detail", args=[tag_id])


def create_user(**args):
    """Create user"""

    return get_user_model().objects.create_user(**args)


def create_tag(user, **kwarg):
    """Create a tag"""

    return Tag.objects.create(user=user, **kwarg)


class PublicTagAPITests(TestCase):
    """Test unauthenticated requests"""

    def test_auth_required(self):
        """Test unauthorized request sent 401 error"""

        client = APIClient()
        response = client.get(TAGS_API_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagApiTests(TestCase):
    """Test for authenticated user"""

    def setUp(self):

        self.client = APIClient()
        self.user = create_user(email="test1@example", password="somepassword")
        self.client.force_authenticate(user=self.user)

    def test_retrieving_tags_list(self):
        """Test retrieving a tag list"""

        for _ in range(2):
            create_tag(user=self.user, name="name")

        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)

        response = self.client.get(TAGS_API_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieving_tag_limited_to_user(self):
        """Test retrieving tag list is limited to authenticated user"""

        create_tag(user=self.user, name="Vegan")
        create_tag(
            user=create_user(email="some@example.com", password="some password"),
            name="Vegetables",
        )

        response = self.client.get(TAGS_API_URL)
        tags = Tag.objects.filter(user=self.user)
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_update_tag(self):
        """Update a tag."""

        tag = create_tag(user=self.user, name="Italian")

        payload = {"name": "Vegan"}

        response = self.client.patch(get_tag_url(tag.id), payload)
        tag.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(tag.name, payload["name"])

    def test_destroy_tag(self):
        """Delete a tag."""

        tag = create_tag(user=self.user, name="Italian")
        response = self.client.delete(get_tag_url(tag.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tag.objects.filter(id=tag.id).exists())
