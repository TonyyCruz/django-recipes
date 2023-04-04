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

        self.assertEquals(response_get.status_code, 404)
        self.assertEquals(response_put.status_code, 404)
        self.assertEquals(response_delete.status_code, 404)
        self.assertEquals(response_patch.status_code, 404)
