from django.forms import ValidationError
from parameterized import parameterized

from .test_testcase_with_recipe import TestCaseWithRecipe


class RecipeModelTest(TestCaseWithRecipe):
    def setUp(self):
        self.recipe = self.make_recipe()
        return super().setUp()

    @parameterized.expand([
        ("title", 65),
        ("description", 165),
        ("preparation_time_unit", 65),
        ("servings_unit", 65),
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, "A" * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()  # valida os campos

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe(
            preparation_steps_is_html=None,
            author=self.make_author(username="user2"),
            slug="user_test2",
        )
        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg="Recipe preparation_steps_is_html is not False",
        )

    def test_recipe_published_is_false_by_default(self):
        recipe = self.make_recipe(
            is_published=None,
            author=self.make_author(username="user2"),
            slug="user_test2"
        )
        self.assertFalse(
            recipe.is_published,
            msg="Recipe is_published is not False",
        )

    def test_recipe_string_representation(self):
        test_title = "Testing Representation"
        self.recipe.title = test_title
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(
            str(self.recipe), test_title,
            msg=f"Recipe string representation must be"
                f"\"{test_title}\" but \"{str(self.recipe)}\" was received."
        )
