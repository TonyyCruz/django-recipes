from django.urls import reverse

from .django_test_case_with_setup import DjangoTestCaseWithSetup


class AuthorsLogoutTest(DjangoTestCaseWithSetup):
    def test_if_logout_raises_302_if_method_is_not_POST(self):  # noqa: E501
        url = reverse("authors:logout")
        response_get = self.client.get(url)
        response_put = self.client.put(url)
        response_delete = self.client.delete(url)
        response_patch = self.client.patch(url)

        self.assertEquals(response_get.status_code, 302)
        self.assertEquals(response_put.status_code, 302)
        self.assertEquals(response_delete.status_code, 302)
        self.assertEquals(response_patch.status_code, 302)
