
import pytest
from selenium.webdriver.common.by import By

from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipesHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipes_home_without_recipes_shows_correct_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, "body")
        self.assertIn("There are no recipes yet", body.text)
