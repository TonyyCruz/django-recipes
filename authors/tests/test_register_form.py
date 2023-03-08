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
        placeholder = form[field].field.widget.attrs["placeholder"]
        self.assertEqual(expect, placeholder)

    @parameterized.expand([
        ("first_name", "First name"),
        ("last_name", "Last name"),
        ("username", "User"),
        ("email", "E-mail"),
        ("password", "Password"),
        ("confirm_password", "Confirm password"),
    ])
    def test_label_is_correct(self, field, expect):
        form = RegisterForm()
        placeholder = form[field].field.label
        self.assertEqual(expect, placeholder)
