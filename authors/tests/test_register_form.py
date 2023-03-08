from django.test import TestCase
from parameterized import parameterized

from authors.forms import RegisterForm


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ("first_name", "Ex.: Ana"),
        ("last_name", "Ex.: Carolina"),
        ("username", "Ex.: @carol"),
        ("email", "Ex.: email@email.com"),
        ("password", "[a-z] [A-Z] [@*!#$%?...]"),
        ("confirm_password", "Repeat you password"),
    ])
    def test_placeholder_is_correct(self, field, expect):
        form = RegisterForm()
        received = form[field].field.widget.attrs["placeholder"]
        self.assertEqual(expect, received)

    @parameterized.expand([
        ("first_name", "First name"),
        ("last_name", "Last name"),
        ("username", "Username"),
        ("email", "E-mail"),
        ("password", "Password"),
        ("confirm_password", "Confirm password"),
    ])
    def test_label_is_correct(self, field, expect):
        form = RegisterForm()
        received = form[field].field.label
        self.assertEqual(expect, received)

    @parameterized.expand([
        (
            "username",
            (
                "Username must have letters, numbers or one of those @.+-_. "
                "The length should be between 4 and 150 characters."
            )
        ),
        (
            "password",
            (
                "Password must have at least 8 characters "
                "containing at least one uppercase, "
                "one lowercase and one special character."
            )
        ),

    ])
    def test_help_text_is_correct(self, field, expect):
        form = RegisterForm()
        received = form[field].field.help_text
        self.assertEqual(expect, received)
