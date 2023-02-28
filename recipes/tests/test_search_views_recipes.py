from django.urls import resolve, reverse

from recipes import views

from .test_testcase_with_recipe import TestCaseWithRecipe


class RecipesSearchViews(TestCaseWithRecipe):
    def test_recipe_search_uses_correct_view(self):
        view = resolve(reverse("recipes:search"))
        self.assertIs(views.search, view.func)

    def test_recipe_search_loads_a_correct_template(self):
        response = self.client.get(reverse("recipes:search") + "?q=test")
        self.assertTemplateUsed(response, "recipes/pages/search.html")

    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse("recipes:search"))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        response = self.client.get(reverse("recipes:search") + "?q=<test>")
        self.assertIn(
            "Search: &quot;&lt;test&gt;&quot;",
            response.content.decode("utf-8"),
        )

    def test_recipe_search_if_raise_404_if_search_term_is_a_space(self):
        response = self.client.get(reverse("recipes:search") + "?q=   ")
        self.assertEqual(response.status_code, 404)
