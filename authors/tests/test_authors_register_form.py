from unittest import TestCase

from django.urls import reverse
from parameterized import parameterized

from authors.forms import RegisterForm

from .django_test_base import DjangoTestCaseWithSetup


# flake8:noqa
class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand(
        [
            ("first_name", "Ex.: Ana"),
            ("last_name", "Ex.: Carolina"),
            ("username", "Ex.: @carol"),
            ("email", "Ex.: email@email.com"),
            ("password", "[a-z] [A-Z] [0-9] [@*!#$%?]"),
            ("confirm_password", "Repeat you password"),
        ]
    )
    def test_placeholder_is_correct(self, field, expect):
        form = RegisterForm()
        received = form[field].field.widget.attrs["placeholder"]
        self.assertEqual(expect, received)

    @parameterized.expand(
        [
            ("first_name", "First name"),
            ("last_name", "Last name"),
            ("username", "Username"),
            ("email", "E-mail"),
            ("password", "Password"),
            ("confirm_password", "Confirm password"),
        ]
    )
    def test_label_is_correct(self, field, expect):
        form = RegisterForm()
        received = form[field].field.label
        self.assertEqual(expect, received)

    @parameterized.expand(
        [
            (
                "username",
                ("The length should be between 4 and 150 characters."),
            ),
            (
                "password",
                (
                    "Password must have at least 8 characters "
                    "containing at least one uppercase, "
                    "one lowercase one number and one special character."
                ),
            ),
        ]
    )
    def test_help_text_is_correct(self, field, expect):
        form = RegisterForm()
        received = form[field].field.help_text
        self.assertEqual(expect, received)


class AuthorRegisterFormIntegrationTest(DjangoTestCaseWithSetup):
    @parameterized.expand(
        [
            ("first_name", "First name must not be empty."),
            ("last_name", "Last name must not be empty."),
            ("username", "Username must not be empty."),
            ("password", "Password must not be empty."),
            ("email", "E-mail must not be empty."),
        ]
    )
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ""
        url = reverse("authors:register_create")
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode("utf-8"))
        self.assertIn(msg, response.context["form"].errors.get(field))

    @parameterized.expand(
        [
            ("abc", "Username must have at least 4 characters."),
            ("a" * 151, "Username must have less than 150 characters."),
        ]
    )
    def test_username_field_cannot_have_length_less_than_4_or_bigger_than_150(
        self, username, msg
    ):
        self.form_data["username"] = username
        url = reverse("authors:register_create")
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode("utf-8"))
        self.assertIn(msg, response.context["form"].errors.get("username"))

    @parameterized.expand(
        [
            ("abcd", "User created successfully"),
            ("a" * 150, "User created successfully"),
        ]
    )
    def test_when_create_a_username_with_a_length_of_4_and_150_characters_have_no_error(
        self, username, msg
    ):
        self.form_data["username"] = username
        url = reverse("authors:register_create")
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode("utf-8"))

    @parameterized.expand(
        [
            ("Abcde9*", "Password must have at least 8 characters."),
            ("abcdef8.", "Password must have at least one uppercase letter."),
            (
                "Abcdefgh9",
                "Password must have at least one special character.",
            ),
            ("ABCDEF9%", "Password must have at least one lowercase letter."),
            ("aBCDEFG#", "Password must have at least one number."),
        ]
    )
    def test_password_field_display_an_error_if_not_have_expected_characters(
        self, password, msg
    ):
        message = msg or (
            "Password must have at least one uppercase letter, "
            "one lowercase letter one number and one special character. "
            "The length should be at least 8 characters."
        )
        self.form_data["password"] = password
        url = reverse("authors:register_create")
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(message, response.context["form"].errors.get("password"))

    def test_confirm_password_field_display_an_error_if_not_equal_to_password_field(
        self,
    ):
        message = '"Password" and "Confirm password" must be equal.'
        self.form_data["password"] = "Password1"
        self.form_data["confirm_password"] = "Password2"
        url = reverse("authors:register_create")
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(
            message, response.context["form"].errors.get("confirm_password")
        )

    @parameterized.expand(
        [
            "Abcdefg9?",
            "aBCDEF5$",
            "aBCDEFGH1!",
        ]
    )
    def test_is_possible_to_create_a_password_with_correct_characters(
        self, password
    ):
        message = "User created successfully"
        self.form_data["password"] = password
        self.form_data["confirm_password"] = password
        url = reverse("authors:register_create")
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(message, response.content.decode("utf-8"))

    def test_register_create_view_raise_a_404_error_if_method_is_not_POST(
        self,
    ):
        url = reverse("authors:register_create")
        response = self.client.get(url, data=self.form_data, follow=True)
        self.assertEqual(response.status_code, 404)

    def test_email_field_must_be_unique(self):
        url = reverse("authors:register_create")
        self.client.post(url, data=self.form_data)
        response = self.client.post(url, data=self.form_data, follow=True)
        content = response.content.decode("utf-8")
        error = response.context["form"].errors.get("email")
        msg = "This email is already in use."

        self.assertIn(msg, content)
        self.assertIn(msg, error)
