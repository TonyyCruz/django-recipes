from django.forms import ValidationError

from .test_testcase_with_recipe import TestCaseWithRecipe


class RecipeModelTest(TestCaseWithRecipe):
    def setUp(self):
        self.recipe = self.make_recipe()
        return super().setUp()

    def test_recipe_title_raise_error_if_title_bigger_than_65_characters(self):
        title_with_100_characters = "A" * 100
        with self.assertRaises(ValidationError):
            self.recipe.title = title_with_100_characters
            self.recipe.full_clean()  # valida os campos
            self.recipe.save()
