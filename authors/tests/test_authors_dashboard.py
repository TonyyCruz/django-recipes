from unittest import TestCase

from django.urls import reverse
from parameterized import parameterized

from authors.forms import RegisterForm

from .django_test_base import DjangoTestCaseWithSetup


# flake8:noqa
class AuthorDashboardIntegrationTest(DjangoTestCaseWithSetup):
    dashboard_url = reverse("authors:dashboard")

    def test_author_dashboard_is_not_accessible_by_unauthorized_user(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)
