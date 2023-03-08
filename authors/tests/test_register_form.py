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
    def test_first_name_placeholder_is_correct(self, field, content):
        form = RegisterForm()
        placeholder = form[field].field.widget.attrs["placeholder"]
        self.assertEqual(content, placeholder)
