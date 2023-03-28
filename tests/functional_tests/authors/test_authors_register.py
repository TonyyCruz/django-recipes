from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .author_functional_base import AuthorBaseFunctionalTest


class AuthorsFunctionalTest(AuthorBaseFunctionalTest):
    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH,
            f'//input[@placeholder="{placeholder}"]'
        )

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, "input")

        for field in fields:
            if field.is_displayed():
                field.send_keys(" " * 20)

    def test_empty_fields_error_message(self):
        self.browser.get(self.live_server_url + "/authors/register/")
        form = self.browser.find_element(
            By.XPATH,
            "/html/body/main/div[2]/form"
        )

        self.fill_form_dummy_data(form=form)
        form.find_element(By.NAME, "email").send_keys("test@email.com")

        first_name_placeholder = self.get_by_placeholder(form, "Ex.: Ana")
        first_name_placeholder.send_keys(" ")
        first_name_placeholder.send_keys(Keys.ENTER)

        form = self.browser.find_element(
            By.XPATH,
            "/html/body/main/div[2]/form"
        )
        self.assertIn("First name must not be empty", form.text)
        self.assertIn("Last name must not be empty", form.text)
        self.assertIn("Username must not be empty", form.text)
        self.assertIn("Password must not be empty", form.text)
        self.assertIn("Confirm password must not be empty", form.text)
