from django.urls import resolve, reverse

from recipes import views

from .recipe_test_base import RecipeTestBase


class RecipesDetailsViews(RecipeTestBase):
    def test_recipe_details_uses_correct_view(self):
        response = resolve(reverse("recipes:details", kwargs={"id": 1}))
        self.assertIs(views.recipe_details, response.func)

    def test_recipe_details_view_return_status_404_if_no_recipe_found(self):
        response = self.client.get(
            reverse("recipes:details", kwargs={"id": 999})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_details_return_status_404_if_recipe_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse("recipes:details", kwargs={"id": recipe.id})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_details_data_is_correct(self):
        author = self.make_author(first_name="Anthony", last_name="Cruz")
        category = self.make_category(name="lanche")
        recipe = self.make_recipe(
            author=author,
            category=category,
            preparation_steps="cozinhar bem",
            preparation_time=5,
            preparation_time_unit="minutos",
            servings=2,
            servings_unit="porções"
        )

        response = self.client.get(
            reverse("recipes:details", kwargs={"id": recipe.id})
        )
        context = response.context["recipe"]
        content = response.content.decode('utf-8')

        self.assertEqual(context.author.first_name, "Anthony")
        self.assertEqual(context.author.last_name, "Cruz")
        self.assertEqual(context.category.name, "lanche")

        self.assertIn("Anthony Cruz", content)
        self.assertIn("<p>cozinhar bem</p>", content)
        self.assertIn("2 porções", content)
        self.assertIn("5 minutos", content)
        self.assertIn("lanche", content)
