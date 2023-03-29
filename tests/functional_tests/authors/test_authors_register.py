from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .author_functional_base import AuthorBaseFunctionalTest


class AuthorsFunctionalTest(AuthorBaseFunctionalTest):
    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH,
            f'//input[@placeholder="{placeholder}"]'
        )

    def fill_form_dummy_data(
        self,
        form,
        first_name="Ana",
        last_name="Carolina",
        username="AnaCarolina",
        email="ana@email.com",
        password="Superp@ss01",
        confirm_password="Superp@ss01",
    ):
        form.find_element(By.NAME, "first_name").send_keys(first_name)
        form.find_element(By.NAME, "last_name").send_keys(last_name)
        form.find_element(By.NAME, "username").send_keys(username)
        form.find_element(By.NAME, "email").send_keys(email)
        form.find_element(By.NAME, "password").send_keys(password)
        form.find_element(
            By.NAME,
            "confirm_password"
        ).send_keys(confirm_password)

    def get_form(self, xpath):
        return self.browser.find_element(
            By.XPATH,
            f"{xpath}"
        )

    # >>>>> TESTS <<<<
    def test_empty_first_name_field_error_message(self):
        self.browser.get(self.live_server_url + "/authors/register/")
        form = self.get_form("/html/body/main/div[2]")

        self.fill_form_dummy_data(form=form, first_name=" " * 10)

        first_name_placeholder = self.get_by_placeholder(form, "Ex.: Ana")
        first_name_placeholder.send_keys(Keys.ENTER)

        form = self.get_form("/html/body/main/div[2]")

        self.assertIn("First name must not be empty", form.text)
        self.assertNotIn("Last name must not be empty", form.text)
        self.assertNotIn("Username must not be empty", form.text)
        self.assertNotIn("Password must not be empty", form.text)
        self.assertNotIn("Confirm password must not be empty", form.text)

    def test_empty_last_name_field_error_message(self):
        self.browser.get(self.live_server_url + "/authors/register/")
        form = self.get_form("/html/body/main/div[2]")

        self.fill_form_dummy_data(form=form, last_name=" " * 10)

        first_name_placeholder = self.get_by_placeholder(form, "Ex.: Carolina")
        first_name_placeholder.send_keys(Keys.ENTER)

        form = self.get_form("/html/body/main/div[2]")

        self.assertNotIn("First name must not be empty", form.text)
        self.assertIn("Last name must not be empty", form.text)
        self.assertNotIn("Username must not be empty", form.text)
        self.assertNotIn("Password must not be empty", form.text)
        self.assertNotIn("Confirm password must not be empty", form.text)
