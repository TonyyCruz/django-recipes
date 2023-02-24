from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    # def test_fake(self):
    #     assert 1 == 1, "Esse texto sera exibido em caso de erro"

    def test_recipe_home_url(self):
        url = reverse("recipes:home")
        self.assertEqual(url, "/")

    def test_recipe_list_url(self):
        url = reverse("recipes:list")
        self.assertEqual(url, "/recipes/")

    def test_recipe_details_url(self):
        url = reverse("recipes:details", kwargs={"id": 1})
        self.assertEqual(url, "/recipe/1/")

    def test_recipe_category_url(self):
        url = reverse("recipes:category", kwargs={"id": 1})
        self.assertEqual(url, "/recipe/category/1/")
