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

    def test_recipe_category_have_a_correct_pagination_range(self):
        """slow"""
        category = self.make_category(name="test_category")
        self.make_multiples_recipes(72, category=category)
        response = self.client.get(
            reverse("recipes:category", kwargs={"id": category.id}) + "?page=1"
        )
        response_2 = self.client.get(
            reverse("recipes:category", kwargs={"id": category.id}) + "?page=3"
        )
        response_3 = self.client.get(
            reverse("recipes:category", kwargs={"id": category.id}) + "?page=4"
        )

        context = response.context["pagination_range"]
        context_2 = response_2.context["pagination_range"]
        context_3 = response_3.context["pagination_range"]

        content = response.content.decode('utf-8')
        content_2 = response_2.content.decode('utf-8')
        content_3 = response_3.content.decode('utf-8')

        self.assertEqual(context["page_range"], range(1, 7))
        self.assertEqual(context["current_page"], 1)
        self.assertEqual(context["stop_range"], 5)
        self.assertIn(
            "<spam class=\"page-link page-item current-page\">1</spam>",
            content
        )

        self.assertEqual(context_2["page_range"], range(1, 7))
        self.assertEqual(context_2["current_page"], 3)
        self.assertEqual(context_2["stop_range"], 5)
        self.assertIn(
            "<spam class=\"page-link page-item current-page\">3</spam>",
            content_2
        )

        self.assertEqual(context_3["page_range"], range(1, 7))
        self.assertEqual(context_3["current_page"], 4)
        self.assertEqual(context_3["stop_range"], 6)
        self.assertIn(
            "<spam class=\"page-link page-item current-page\">4</spam>",
            content_3
        )
