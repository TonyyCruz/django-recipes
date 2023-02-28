from django.urls import resolve, reverse

from recipes import views

from .test_testcase_with_recipe import TestCaseWithRecipe


class RecipesListViews(TestCaseWithRecipe):
    def test_recipe_list_uses_correct_view(self):
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
