
from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .recipe_functional_base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipesHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipes_home_without_recipes_shows_correct_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, "body")
        self.assertIn("There are no recipes yet", body.text)

    @patch("recipes.views.ITEMS_PER_PAGE", new=2)
    @patch("recipes.views.QTY_PAGES_IN_PAGINATION", new=5)
    def test_recipe_search_input_can_find_correct_recipe(self):
        self.make_multiples_recipes(
            quantity=10, title="Recipe test", stack_name="test")
        self.make_multiples_recipes(
            quantity=1, title="Recipe test1", stack_name="test1")
        self.make_multiples_recipes(
            quantity=2, title="Recipe test2", stack_name="test2")
        self.make_multiples_recipes(
            quantity=3, title="Recipe test3", stack_name="test3")

        self.browser.get(self.live_server_url)

        # TEST "Recipe test1"
        search_input = self.browser.find_element(
            By.XPATH,
            "//input[@placeholder='Search for a recipe...']"
        )
        search_input.send_keys("Recipe test1")
        search_input.send_keys(Keys.ENTER)

        self.assertIn(
            "Recipe test1",
            self.browser.find_element(By.TAG_NAME, "body").text
        )
        self.assertEqual(
            1,
            len(self.browser.find_elements(By.CLASS_NAME, "recipe-title"))
        )

        # TEST "Recipe test2"
        search_input = self.browser.find_element(
            By.XPATH,
            "//input[@placeholder='Search for a recipe...']"
        )

        search_input.send_keys("Recipe test2")
        search_input.send_keys(Keys.ENTER)

        self.assertIn(
            "Recipe test2",
            self.browser.find_element(By.TAG_NAME, "body").text
        )
        self.assertEqual(
            2,
            len(self.browser.find_elements(By.CLASS_NAME, "recipe-title"))
        )

        # TEST "Recipe test3"
        search_input = self.browser.find_element(
            By.XPATH,
            "//input[@placeholder='Search for a recipe...']"
        )

        search_input.send_keys("Recipe test3")
        search_input.send_keys(Keys.ENTER)

        self.assertIn(
            "Recipe test3",
            self.browser.find_element(By.TAG_NAME, "body").text
        )
        self.assertEqual(
            2,
            len(self.browser.find_elements(By.CLASS_NAME, "recipe-title"))
        )

        page_two = self.browser.find_elements(
            By.CLASS_NAME,
            "page-link"
        )[1]

        self.assertEqual(page_two.text, "2")
        page_two.click()

        self.assertIn(
            "Recipe test3",
            self.browser.find_element(By.TAG_NAME, "body").text
        )
        self.assertEqual(
            1,
            len(self.browser.find_elements(By.CLASS_NAME, "recipe-title"))
        )

    # TEST "Recipe test"
        search_input = self.browser.find_element(
            By.XPATH,
            "//input[@placeholder='Search for a recipe...']"
        )

        search_input.send_keys("Recipe")
        search_input.send_keys(Keys.ENTER)

        self.assertIn(
            "Recipe",
            self.browser.find_element(By.TAG_NAME, "body").text
        )
        self.assertEqual(
            2,
            len(self.browser.find_elements(By.CLASS_NAME, "recipe-title"))
        )
        self.assertEqual(
            6,
            len(self.browser.find_elements(By.CLASS_NAME, "page-link"))
        )

        page_four = self.browser.find_elements(
            By.CLASS_NAME,
            "page-link"
        )[3]
        self.assertEqual(page_four.text, "4")

        page_four.click()

        self.assertIn(
            "Recipe",
            self.browser.find_element(By.TAG_NAME, "body").text
        )
        self.assertEqual(
            2,
            len(self.browser.find_elements(By.CLASS_NAME, "recipe-title"))
        )
        self.assertEqual(
            7,
            len(self.browser.find_elements(By.CLASS_NAME, "page-link"))
        )
        self.assertEqual(
            "2",
            self.browser.find_elements(By.CLASS_NAME, "page-link")[1].text
        )
        self.assertEqual(
            "6",
            self.browser.find_elements(By.CLASS_NAME, "page-link")[5].text
        )

        last_page = self.browser.find_elements(
            By.CLASS_NAME,
            "page-link"
        )[6]
        self.assertIn("8", last_page.text)

        last_page.click()

        self.assertIn(
            "Recipe",
            self.browser.find_element(By.TAG_NAME, "body").text
        )
        self.assertEqual(
            2,
            len(self.browser.find_elements(By.CLASS_NAME, "recipe-title"))
        )
        self.assertEqual(
            6,
            len(self.browser.find_elements(By.CLASS_NAME, "page-link"))
        )
        self.assertEqual(
            "4",
            self.browser.find_elements(By.CLASS_NAME, "page-link")[1].text
        )
        self.assertEqual(
            "8",
            self.browser.find_elements(By.CLASS_NAME, "page-link")[5].text
        )
