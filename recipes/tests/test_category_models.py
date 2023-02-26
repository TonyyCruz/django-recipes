from django.forms import ValidationError

from .test_testcase_with_recipe import TestCaseWithRecipe


class CategoryModelTest(TestCaseWithRecipe):
    def setUp(self):
        self.category = self.make_category(
            name="test"
        )
        return super().setUp()

    def test_recipe_category_model_string_representation_is_name_field(self):
        self.assertEqual(
            str(self.category),
            self.category.name
        )

    def test_recipe_category_model_name_max_length_is_65_chars(self):
        self.category.name = 'A' * 66
        with self.assertRaises(ValidationError):
            self.category.full_clean()
