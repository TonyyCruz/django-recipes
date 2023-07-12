from unittest import TestCase

from django.urls import reverse
from parameterized import parameterized

from authors.forms import RegisterForm

from .django_test_base import DjangoTestCaseWithSetup


# flake8:noqa
class AuthorDashboardIntegrationTest(DjangoTestCaseWithSetup):
    dashboard_url = reverse("authors:dashboard")
    dashboard_recipe_create_url = reverse("authors:dashboard_recipe_create")

    def test_author_dashboard_is_not_accessible_by_unauthenticated_user(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)

    def test_author_dashboard_unauthenticated_user_is_redirect_to_login(self):
        response = self.client.get(self.dashboard_url, follow=True)

        content = response.content.decode("utf-8")

        self.assertIn("Login", content)
        self.assertNotIn("Dashboard", content)

    def test_author_dashboard_authenticated_user_can_access_dashboard(self):
        self.login_dummy_user()

        response = self.client.get(self.dashboard_url)

        content = response.content.decode("utf-8")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Dashboard", content)

    def test_author_dashboard_authenticated_user_can_create_a_recipe(self):
        self.login_dummy_user()

        response = self.client.post(
            self.dashboard_recipe_create_url, data=self.mock_recipe_dict
        )

        content = response.content.decode("utf-8")

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.mock_recipe_dict["title"], content)
