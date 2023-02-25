from django.urls import resolve, reverse

from recipes import views

from .test_recipe_setup import TestCaseWithSetup

# from pytest import skip  # é um dacorator para pular o teste: @skip()


class RecipeViewsTest(TestCaseWithSetup):
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
        self.make_recipe()
        response = self.client.get(reverse("recipes:list"))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertIn('My test title', content)
        self.assertIn('10 minutos', content)
        self.assertIn('3 porcoes', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_list_no_published_recipes_not_appear(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse("recipes:list"))
        content = response.content.decode('utf-8')

        self.assertIn('Não há nenhuma receita ainda', content)
