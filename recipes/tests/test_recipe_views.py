from django.test import TestCase
from django.urls import resolve, reverse

from recipes import views


class RecipeViewsTest(TestCase):
    def test_recipe_view_home_is_correct(self):
        view = resolve(reverse("recipes:home"))
        self.assertIs(views.home, view.func)

    def test_recipe_view_recipes_is_correct(self):
        view = resolve(reverse("recipes:list"))
        self.assertIs(views.recipe_list, view.func)

    def test_recipe_view_details_is_correct(self):
        view = resolve(reverse("recipes:details", kwargs={"id": 1}))
        self.assertIs(views.recipe_details, view.func)

    def test_recipe_view_category_is_correct(self):
        view = resolve(reverse("recipes:category", kwargs={"id": 1}))
        self.assertIs(views.category, view.func)
