from core.models import User
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")


def create_user(**user_data) -> User:
    return get_user_model().objects.create_user(**user_data)


class TestPublicUserEndpoints(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_user_create_successfully(self):
        """Test if user is created succesfully"""

        payload = {
            "email": "test@example.com",
            "name": "somename",
            "password": "testpassword1234",
        }

        response = self.client.post(CREATE_USER_URL, payload)
        user = get_user_model().objects.get(email=payload["email"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", response.data)

    def test_user_create_already_exists(self):
        """Test if user was not created when email is already exists in db"""
        payload = {
            "email": "test@example.com",
            "name": "somename",
            "password": "testpassword1234",
        }

        create_user(**payload)
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_create_too_short_password(self):
        """Test if user was not created when password is too shorr (shorter than 5 char)"""

        payload = {
            "email": "test@example.com",
            "name": "asasa",
            "password": "2324",
        }

        response = self.client.post(CREATE_USER_URL, payload)
        is_user_exist = get_user_model().objects.filter(email=payload["email"]).exists()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(is_user_exist)

    def test_create_token_for_user(self):
        """It should return token when credentials are ok"""

        user_data = {
            "name": "Test Name",
            "password": "testpassword",
            "email": "test@example.com",
        }

        token_request_payload = {
            "email": user_data["email"],
            "password": user_data["password"],
        }

        create_user(**user_data)
        response = self.client.post(TOKEN_URL, token_request_payload)

        self.assertIn(member="token", container=response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """It should return an error instead of token when credentials are bad"""

        payload = {
            "email": "test2@example.com",
            "password": "12344",
        }

        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn(member="token", container=response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_empty_password(self):
        """It should return an error instead of token when password is empty"""

        user_data = {
            "name": "test data",
            "password": "password",
            "email": "test@example.com",
        }
        token_request_payload = {"email": user_data["email"], "password": ""}

        create_user(**user_data)
        response = self.client.post(TOKEN_URL, token_request_payload)

        self.assertNotIn(member="token", container=response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
