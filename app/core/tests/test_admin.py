from django.contrib.auth import get_user_model  # noqa
from django.test import TestCase  # noqa
from django.test import Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        user_manager = get_user_model().objects
        self.client = Client()
        self.admin = user_manager.create_superuser(
            email="admin@example.com", password="somepassword1234"
        )
        self.user = user_manager.create_user(
            email="user@example.com", password="testpass123", name="Test User"
        )

        self.client.force_login(self.admin)

    def test_user_list(self):
        """Test that users are visible on the admin page"""

        url = reverse("admin:core_user_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.user.email)
        self.assertContains(response, self.user.name)

    def test_edit_user_page(self):
        """Test if user edit page works on admin panel"""

        url = reverse("admin:core_user_change", args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_create_user_page(self):
        """Test if creating user page works"""

        url = reverse("admin:core_user_add")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
