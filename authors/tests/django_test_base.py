from django.test import TestCase as DjangoTestCase
from django.urls import reverse


class DjangoTestCaseWithSetup(DjangoTestCase):
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

    def create_dummy_user(self):
        return self.client.post(
            reverse("authors:register_create"),
            data=self.form_data,
        )

    def login_dummy_user(self):
        return self.client.login(
            username=self.form_data["username"],
            password=self.form_data["password"],
        )
