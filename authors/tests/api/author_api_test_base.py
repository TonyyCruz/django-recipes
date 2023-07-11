from django.urls import reverse
from rest_framework import test

from recipes.tests.recipe_test_base import RecipeMixing


class AuthorApiMixing(RecipeMixing):
    author_api_url = reverse("authors:author-api-list")
    author_api_token_obtain = reverse("recipes:token_obtain_pair")
    author_api_token_verify = reverse("recipes:token_verify")

    def get_author_response(self, id=""):
        return self.client.get(self.author_api_url + id)


class AuthorApiTestBase(test.APITestCase, AuthorApiMixing):
    def setUp(self):
        return super().setUp()

    def get_auth_data(
        self,
        user={"username": "dev01", "password": "Password1!"},
    ):
        author = self.make_author(**user)

        jwt_token = self.client.post(
            self.recipe_api_token_obtain,
            {"username": user["username"], "password": user["password"]},
        )

        return {**jwt_token.data, "author": author}
