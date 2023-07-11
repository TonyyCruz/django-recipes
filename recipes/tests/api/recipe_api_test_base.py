from django.urls import reverse
from rest_framework import test

from recipes.tests.recipe_test_base import RecipeMixing


class RecipeApiMixing(RecipeMixing):
    recipe_api_list_url = reverse("recipes:recipes-api-list")
    recipe_api_token_obtain = reverse("recipes:token_obtain_pair")
    recipe_api_token_verify = reverse("recipes:token_verify")

    def get_recipe_list_response(self, page="1", url_query=None):
        if url_query:
            page = page + f"&{url_query}"

        return self.client.get(self.recipe_api_list_url + f"?page={page}")


class RecipeApiTestBase(test.APITestCase, RecipeApiMixing):
    def setUp(self):
        return super().setUp()

    def get_token(self, **kwargs):
        username = kwargs.get("username", "dev01")
        password = kwargs.get("password", "Password1!")

        token = self.client.post(
            self.recipe_api_token_obtain,
            {"username": username, "password": password},
        )
        return token.data

    def get_auth_data(self, **kwargs):
        username = kwargs.get("username", "dev01")
        password = kwargs.get("password", "Password1!")

        # cria um author com o username e password recebido
        author = self.make_author(username=username, password=password)
        jwt_token = self.get_token(username=username, password=password)

        # jwt_token.data have "refresh" and "access" token.
        return {**jwt_token, "author": author}
