from django.urls import reverse

from .django_test_case_with_setup import DjangoTestCaseWithSetup


class LoginFormTest(DjangoTestCaseWithSetup):
    def create_dummy_user(self):
        return self.client.post(
            reverse("authors:register_create"),
            data=self.form_data,
        )

    def test_author_created_can_login(self):
        self.create_dummy_user()
        can_login = self.client.login(
            username=self.form_data["username"],
            password=self.form_data["password"],
        )

        self.assertTrue(can_login)

    def test_if_login_create_chows_a_not_found_message_if_the_method_received_is_not_POST(self):  # noqa: E501
        expected_text = "Not Found"
        url = reverse("authors:login_create")
        response_get = self.client.get(url)
        response_put = self.client.put(url)
        response_delete = self.client.delete(url)
        response_patch = self.client.patch(url)

        self.assertIn(expected_text, response_get.content.decode("utf-8"))
        self.assertIn(expected_text, response_put.content.decode("utf-8"))
        self.assertIn(expected_text, response_delete.content.decode("utf-8"))
        self.assertIn(expected_text, response_patch.content.decode("utf-8"))
