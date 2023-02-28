from django.urls import resolve, reverse

from recipes import views

from .test_testcase_with_recipe import TestCaseWithRecipe


class RecipesCategoryViews(TestCaseWithRecipe):
    def test_recipe_category_uses_correct_view(self):
        view = resolve(reverse("recipes:category", kwargs={"id": 1}))
        self.assertIs(views.category, view.func)

    def test_recipe_category_view_return_status_404_if_no_recipe_found(self):
        response = self.client.get(
            reverse("recipes:category", kwargs={"id": 999}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_return_status_404_if_recipe_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse("recipes:category", kwargs={"id": recipe.category.id}))
        self.assertEqual(response.status_code, 404)
