import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .author_functional_base import AuthorBaseFunctionalTest


@pytest.mark.functional_test
class AuthorsLoginFunctionalTest(AuthorBaseFunctionalTest):
    def test_if_it_is_possible_to_login(self):
        username = "testname"
        password = "MySecr3tPass!"
        User.objects.create_user(
            username=username, password=password
        )
        self.browser.get(self.live_server_url + reverse("authors:login"))

        login_form = self.get_form(class_name="main-form")
        login_form.find_element(By.NAME, "username").send_keys(username)
        login_form.find_element(By.NAME, "password").send_keys(password)

        login_form.submit()

        recipes_page = self.browser.find_element(By.TAG_NAME, "body")
        self.assertNotIn("Login", recipes_page.text)
        self.assertIn("There are no recipes yet", recipes_page.text)

    def test_login_invalid_username_shows_login_error_message(self):
        correct_username = "testname"
        correct_password = "MySecr3tPass!"
        invalid_username = "testwrong"

        User.objects.create_user(
            username=correct_username, password=correct_password
        )

        self.browser.get(self.live_server_url + reverse("authors:login"))

        login_form = self.get_form(class_name="main-form")
        login_form.find_element(
            By.NAME,
            "username"
        ).send_keys(invalid_username)

        login_form.find_element(
            By.NAME,
            "password"
        ).send_keys(correct_password)

        login_form.submit()

        login_page = self.browser.find_element(By.TAG_NAME, "body")
        self.assertIn("Invalid username or password", login_page.text)

    def test_login_invalid_password_shows_login_error_message(self):
        correct_username = "testname"
        correct_password = "MySecr3tPass!"
        invalid_password = "Inv4lidPass?"

        User.objects.create_user(
            username=correct_username, password=correct_password
        )

        self.browser.get(self.live_server_url + reverse("authors:login"))

        login_form = self.get_form(class_name="main-form")
        login_form.find_element(
            By.NAME,
            "username"
        ).send_keys(correct_username)

        login_form.find_element(
            By.NAME,
            "password"
        ).send_keys(invalid_password)

        login_form.submit()

        login_page = self.browser.find_element(By.TAG_NAME, "body")
        self.assertIn("Invalid username or password", login_page.text)

    def test_login_invalid_invalid_form_data_message(self):
        username = " " * 10
        password = " " * 10

        User.objects.create_user(
            username=username, password=password
        )

        self.browser.get(self.live_server_url + reverse("authors:login"))

        login_form = self.get_form(class_name="main-form")
        login_form.find_element(
            By.NAME,
            "username"
        ).send_keys(username)

        login_form.find_element(
            By.NAME,
            "password"
        ).send_keys(password)

        login_form.submit()

        login_page = self.browser.find_element(By.TAG_NAME, "body")
        self.assertIn("Invalid credentials", login_page.text)
