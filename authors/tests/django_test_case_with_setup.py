from django.test import TestCase as DjangoTestCase


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
