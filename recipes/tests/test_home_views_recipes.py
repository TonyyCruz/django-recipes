from django.urls import resolve, reverse

from recipes import views

from .test_testcase_with_recipe import TestCaseWithRecipe


class RecipesHomeViews(TestCaseWithRecipe):
    def test_recipe_home_uses_correct_view(self):
        view = resolve(reverse("recipes:home"))
        self.assertIs(views.home, view.func)

    def test_recipe_home_view_return_status_code_200(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertTemplateUsed(response, "recipes/pages/home.html")
