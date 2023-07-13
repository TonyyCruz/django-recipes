from django.urls import reverse

from .django_test_base import DjangoTestCaseWithSetup


class AuthorsLogoutTest(DjangoTestCaseWithSetup):
    def test_if_logout_redirect_to_login_if_method_is_not_POST(self):
        self.create_dummy_user()
        self.login_dummy_user()
        url = reverse("authors:logout")
        response_get = self.client.get(url)
        response_put = self.client.put(url)
        response_delete = self.client.delete(url)
        response_patch = self.client.patch(url)

        self.assertEqual(response_get.status_code, 404)
        self.assertEqual(response_put.status_code, 404)
        self.assertEqual(response_delete.status_code, 404)
        self.assertEqual(response_patch.status_code, 404)

    def test_logout_with_another_user(self):
        self.create_dummy_user()
        self.login_dummy_user()
        response = self.client.post(
            reverse("authors:logout"),
            data={"username": "incorrectUser"},
            follow=True,
        )

        self.assertEqual(response.status_code, 404)

    def test_logout_successfully(self):
        self.create_dummy_user()
        self.login_dummy_user()
        response = self.client.post(
            reverse("authors:logout"), data=self.form_data, follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Successfully logged out",
            response.content.decode("utf-8"),
        )
