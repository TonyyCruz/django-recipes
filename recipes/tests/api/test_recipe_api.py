from unittest.mock import patch

from django.urls import reverse
from rest_framework import test

from recipes.tests.recipe_test_base import RecipeMixing


# flake8: noqa
class RecipeAPIv2Test(test.APITestCase, RecipeMixing):
    recipe_api_list_url = reverse("recipes:recipes-api-list")

    def recipe_list_response(self, page="1"):
        return self.client.get(self.recipe_api_list_url + f"?page={page}")

    def test_recipe_api_list_returns_status_code_200(self):
        self.assertAlmostEqual(self.recipe_list_response().status_code, 200)

    @patch("recipes.views.api.RecipeAPIv2Pagination.page_size", new=3)
    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        total_number_of_recipes = 7
        max_number_of_recipes_per_Page = 3
        wanted_recipes_in_third_page = 1
        self.make_multiples_recipes(quantity=total_number_of_recipes)
        qty_of_loaded_recipes_first_page = len(
            self.recipe_list_response().data.get("results")
        )
        qty_of_loaded_recipes_second_page = len(
            self.recipe_list_response(page=2).data.get("results")
        )
        qty_of_loaded_recipes_third_page = len(
            self.recipe_list_response(page=3).data.get("results")
        )

        self.assertEqual(
            max_number_of_recipes_per_Page,
            qty_of_loaded_recipes_first_page,
        )
        self.assertEqual(
            max_number_of_recipes_per_Page,
            qty_of_loaded_recipes_second_page,
        )
        self.assertEqual(
            wanted_recipes_in_third_page,
            qty_of_loaded_recipes_third_page,
        )
