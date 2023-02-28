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

    def test_recipe_search_can_find_recipe_by_title(self):
        title_1 = "Farofa de batata com queijo"
        title_2 = "Lasanha de carne com queijo"
        recipe_1 = self.make_recipe(
            title=title_1,
            slug="farofa",
            author=self.make_author(username="user1")
        )
        recipe_2 = self.make_recipe(
            title=title_2,
            slug="lasanha",
            author=self.make_author(username="user2")
        )

        search_url = reverse("recipes:search")
        response_1 = self.client.get(f"{search_url}?q=farofa")
        response_2 = self.client.get(f"{search_url}?q=lasanha")
        response_both = self.client.get(f"{search_url}?q=queijo")

        self.assertIn(recipe_1, response_1.context["recipes"])
        self.assertNotIn(recipe_1, response_2.context["recipes"])

        self.assertIn(recipe_2, response_2.context["recipes"])
        self.assertNotIn(recipe_2, response_1.context["recipes"])

        self.assertIn(recipe_1, response_both.context["recipes"])
        self.assertIn(recipe_2, response_both.context["recipes"])

    def test_recipe_search_not_show_no_published_recipes(self):
        recipe = self.make_recipe(is_published=False)
        search_url = reverse("recipes:search")
        response = self.client.get(f"{search_url}?q=something")

        self.assertNotIn(recipe, response.context["recipes"])
