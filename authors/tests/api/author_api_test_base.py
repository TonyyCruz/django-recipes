from django.urls import reverse

from recipes.tests.api.recipe_api_test_base import RecipeApiTestBase


class AuthorApiTestBase(RecipeApiTestBase):
    author_api_url = reverse("authors:author-api-list")
    author_api_token_obtain = reverse("recipes:token_obtain_pair")
    author_api_token_verify = reverse("recipes:token_verify")

    def get_author_response(self, id=""):
        return self.client.get(self.author_api_url + id)
