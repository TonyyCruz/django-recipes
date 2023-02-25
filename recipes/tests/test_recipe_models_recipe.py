from .test_testcase_with_recipe import TestCaseWithRecipe


class RecipeModelTest(TestCaseWithRecipe):
    def setUp(self):
        self.recipe = self.make_recipe()
        return super().setUp()
