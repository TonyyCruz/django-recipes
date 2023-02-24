from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from recipes import views
from recipes.models import Category, Recipe


class RecipeViewsTest(TestCase):
    #   ===== HOME =====
    def test_recipe_view_home_is_correct(self):
        view = resolve(reverse("recipes:home"))
        self.assertIs(views.home, view.func)

    def test_recipe_home_view_return_status_code_200(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertTemplateUsed(response, "recipes/pages/home.html")

    #   ===== CATEGORY =====
    def test_recipe_view_category_is_correct(self):
        view = resolve(reverse("recipes:category", kwargs={"id": 1}))
        self.assertIs(views.category, view.func)

    def test_recipe_category_view_return_status_404_if_no_recipe_found(self):
        response = self.client.get(
            reverse("recipes:category", kwargs={"id": 999}))
        self.assertEqual(response.status_code, 404)

    #   ===== DETAILS =====
    def test_recipe_list_view_details_is_correct(self):
        view = resolve(reverse("recipes:details", kwargs={"id": 1}))
        self.assertIs(views.recipe_details, view.func)

    def test_recipe_details_view_return_status_404_if_no_recipe_found(self):
        response = self.client.get(
            reverse("recipes:details", kwargs={"id": 999}))
        self.assertEqual(response.status_code, 404)

    #   ===== RECIPE LIST =====
    def test_recipe_list_view_recipes_is_correct(self):
        view = resolve(reverse("recipes:list"))
        self.assertIs(views.recipe_list, view.func)

    def test_recipe_list_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse("recipes:list"))
        self.assertIn(
            '<h1>Não há nenhuma receita ainda</h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_list_loads_recipe(self):
        category = Category.objects.create(name="category_name")
        author = User.objects.create_user(
            first_name="user",
            last_name="name",
            username="user_name",
            password="123456",
            email="user@user.com",
        )
        Recipe.objects.create(
            category=category,
            author=author,
            title="My test title",
            description="description",
            slug="slug",
            preparation_time=10,
            preparation_time_unit="minutos",
            servings=3,
            servings_unit="porcoes",
            preparation_steps="cozinha e come",
            preparation_steps_is_html=False,
            is_published=True,
        )
        response = self.client.get(reverse("recipes:list"))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertIn('My test title', content)
        self.assertIn('10 minutos', content)
        self.assertIn('3 porcoes', content)
        self.assertEqual(len(response_context_recipes), 1)
