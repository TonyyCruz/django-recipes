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

    def test_if_login_create_raises_404_if_method_is_not_POST(self):  # noqa: E501
        url = reverse("authors:login_create")
        response_get = self.client.get(url)
        response_put = self.client.put(url)
        response_delete = self.client.delete(url)
        response_patch = self.client.patch(url)

        self.assertEquals(response_get.status_code, 404)
        self.assertEquals(response_put.status_code, 404)
        self.assertEquals(response_delete.status_code, 404)
        self.assertEquals(response_patch.status_code, 404)

    # def test_invalid_password_or_username_shows_error_message(self):
    #     self.create_dummy_user()
    #     url = reverse("authors:login_create")
    #     response = self.client.post(
    #         url,
    #         username=self.form_data["username"],
    #         password="wrongPass1",
    #     )
    #     response
