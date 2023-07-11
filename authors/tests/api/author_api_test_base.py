import json

from django.urls import reverse

from recipes.tests.api.recipe_api_test_base import RecipeApiTestBase


class AuthorApiTestBase(RecipeApiTestBase):
    author_api_url = reverse("authors:author-api-list")
    author_api_token_obtain = reverse("recipes:token_obtain_pair")
    author_api_token_verify = reverse("recipes:token_verify")

    def get_author_response(self, id="", token="", **kw):
        patch = f"{self.author_api_url}{id}/" if id else self.author_api_url

        return self.client.get(
            path=patch,
            HTTP_AUTHORIZATION=f"Bearer {token}" if token else "",
            **kw,
        )

    def post_author_response(self, data={}, token="", **kw):
        return self.client.post(
            path=self.author_api_url,
            data=json.dumps(data),
            HTTP_AUTHORIZATION=f"Bearer {token}" if token else "",
            content_type="application/json",
            **kw,
        )

    def patch_author_response(self, data, token, id, **kw):
        patch = f"{self.author_api_url}{id}/"
        return self.client.patch(
            path=patch,
            data=json.dumps(data),
            HTTP_AUTHORIZATION=f"Bearer {token}",
            content_type="application/json",
            **kw,
        )

    def delete_author_response(self, token, id, **kw):
        patch = f"{self.author_api_url}{id}/"
        return self.client.delete(
            path=patch,
            HTTP_AUTHORIZATION=f"Bearer {token}",
            content_type="application/json",
            **kw,
        )
