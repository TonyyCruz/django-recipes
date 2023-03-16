from time import sleep

from django.test import LiveServerTestCase

from utils.browser import make_chrome_browser

# from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class RecipeBaseFunctionalTest(LiveServerTestCase):
    def setUp(self):
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self):
        self.browser.quit()
        return super().tearDown()

    def sleep(self, time=5):
        sleep(time)
