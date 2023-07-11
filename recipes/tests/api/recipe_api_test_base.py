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

    def get_auth_data(
        self,
        user={"username": "dev01", "password": "Password1!"},
    ):
        author = self.make_author(**user)

        jwt_token = self.client.post(
            self.recipe_api_token_obtain,
            {"username": user["username"], "password": user["password"]},
        )
        # jwt_token.data have "refresh" and "access" token.
        return {**jwt_token.data, "author": author}
