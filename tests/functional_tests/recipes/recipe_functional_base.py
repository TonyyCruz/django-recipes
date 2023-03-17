from time import sleep

from django.test import LiveServerTestCase

# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from recipes.tests.recipe_test_base import RecipeMixing
from utils.browser import make_chrome_browser


class RecipeBaseFunctionalTest(LiveServerTestCase, RecipeMixing):
    def setUp(self):
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self):
        self.browser.quit()
        return super().tearDown()

    def sleep(self, time=5):
        sleep(time)
