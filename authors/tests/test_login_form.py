from django.urls import reverse

from .django_test_base import DjangoTestCaseWithSetup


class LoginFormTest(DjangoTestCaseWithSetup):
    def test_author_created_can_login(self):
        self.create_dummy_user()
        can_login = self.login_dummy_user()

        self.assertTrue(can_login)

    def test_if_login_create_raises_404_if_method_is_not_POST(self):
        url = reverse("authors:login_create")
        response_get = self.client.get(url)
        response_put = self.client.put(url)
        response_delete = self.client.delete(url)
        response_patch = self.client.patch(url)

        self.assertEquals(response_get.status_code, 404)
        self.assertEquals(response_put.status_code, 404)
        self.assertEquals(response_delete.status_code, 404)
        self.assertEquals(response_patch.status_code, 404)
