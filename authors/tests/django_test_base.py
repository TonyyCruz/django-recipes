from django.test import TestCase as DjangoTestCase
from django.urls import reverse

from recipes.tests.recipe_test_base import RecipeMixing


class DjangoTestCaseWithSetup(DjangoTestCase, RecipeMixing):
    def setUp(self):
        self.form_data = {
            "username": "user",
            "first_name": "first",
            "last_name": "last",
            "email": "email@email.com",
            "password": "Str0ngP@ssword1",
            "confirm_password": "Str0ngP@ssword1",
        }
        return super().setUp()

    def create_dummy_user(self, user_data=None):
        if user_data is None:
            user_data = self.form_data

        return self.client.post(
            reverse("authors:register_create"),
            data=user_data,
        )

    def login_dummy_user(self, username=None, password=None):
        if username is None:
            username = self.form_data["username"]

        if password is None:
            password = self.form_data["password"]

        return self.client.login(
            username=username,
            password=password,
        )
