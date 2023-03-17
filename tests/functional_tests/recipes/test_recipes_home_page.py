
import pytest
from selenium.webdriver.common.by import By

from .recipe_functional_base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipesHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipes_home_without_recipes_shows_correct_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, "body")
        self.assertIn("There are no recipes yet", body.text)

    def test_search_input(self):
        self.make_multiples_recipes(quantity=1, title="test1")
        self.make_multiples_recipes(quantity=2, title="test2")
        self.make_multiples_recipes(quantity=3, title="test3")
        ...
