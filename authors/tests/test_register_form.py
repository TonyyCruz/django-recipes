from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
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
                "one lowercase and one special character or number."
            )
        ),

    ])
    def test_help_text_is_correct(self, field, expect):
        form = RegisterForm()
        received = form[field].field.help_text
        self.assertEqual(expect, received)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self):
        self.form_data = {
            "username": "user",
            "first_name": "first",
            "last_name": "last",
            "email": "email@email.com",
            "password": "Str0ngP@ssword1",
            "confirm_password": "Str0ngP@ssword1",
        }
        return super().setUp()

    @parameterized.expand([
        ("first_name", "This field must not be empty"),
        ("last_name", "This field must not be empty"),
        ("username", "This field must not be empty"),
        ("password", "This field must not be empty"),
        ("email", "This field must not be empty"),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ""
        url = reverse("authors:create")
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode("utf-8"))
