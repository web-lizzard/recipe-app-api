"""
Test user model
"""


from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTest(TestCase):
    def test_create_user_with_email_succesfully(self):
        email = "test@example.com"
        password = "testpassword1234"
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(email, user.email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):
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
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email="", password="sample")

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            email="test@example.com", password="samplepassword"
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
