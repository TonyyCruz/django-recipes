# import json

# from parameterized import parameterized

from .author_api_test_base import AuthorApiTestBase

# from unittest.mock import patch


# flake8:noqa
class AuthorsAPIv2Test(AuthorApiTestBase):
    def test_author_api_anonymous_get_method_receive_status_code_401(self):
        response = self.get_author_response()
        self.assertAlmostEqual(response.status_code, 401)
