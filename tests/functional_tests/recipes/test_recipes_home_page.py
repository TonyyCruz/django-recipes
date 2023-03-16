
from selenium.webdriver.common.by import By

from tests.functional_tests.recipes.recipe_base_live_server_test import \
    RecipeBaseFunctionalTest


class RecipesHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipes_home_without_recipes_shows_correct_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, "body")
        self.assertIn("There are no recipes yet", body.text)
