"""
Test user model
"""
from decimal import Decimal

from core import models
from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTest(TestCase):
    """Tests for models"""

    manager = get_user_model().objects

    def test_create_user_with_email_successfully(self):
        """Test creating user with proper email"""
        email = "test@example.com"
        password = "testpassword1234"
        user = self.manager.create_user(email=email, password=password)

        self.assertEqual(email, user.email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):
        """test normalize email before creating a new user"""
        sample_tests = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for email, expected in sample_tests:
            user = get_user_model().objects.create_user(
                email=email, password="sample12345"
            )

            self.assertEqual(user.email, expected)

    def test_user_without_email_raises_value_exception(self):
        """Test raising an error when email field is empty"""

        with self.assertRaises(ValueError):
            self.manager.create_user(email="", password="sample")

    def test_create_superuser(self):
        """Test creating super user (with admin permission)"""

        user = self.manager.create_superuser(
            email="test@example.com", password="samplepassword"
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_recipe(self):
        """Test Creating recipe is successful."""

        user = get_user_model().objects.create_user("test@example.com", "testpass1234")
        recipe = models.Recipe.objects.create(
            user=user,
            title="Recipe name",
            time_minutes=5,
            price=Decimal("5.50"),
            description="Sample recipe description",
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating tag is successful"""

        user = get_user_model().objects.create_user("test5@example.com", "testpass1234")
        tag = models.Tag.objects.create(user=user, name="A Tag name")

        self.assertEqual(str(tag), tag.name)
