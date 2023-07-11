# import json

# from parameterized import parameterized

from .author_api_test_base import AuthorApiTestBase

# from unittest.mock import patch


# flake8:noqa
class AuthorsAPIv2Test(AuthorApiTestBase):
    def test_author_api_anonymous_get_method_receive_status_code_401(self):
        response = self.get_author_response()
        self.assertAlmostEqual(response.status_code, 401)

    def test_author_api_cannot_get_data_of_another_user(self):
        # cria o primeiro usuario (id = 1)
        user_auth = self.get_auth_data()
        # pega o token do user
        user_token = user_auth.get("access", "")

        # cria o segundo usuario (id = 2)
        another_user = self.get_auth_data(
            user={"username": "usr", "password": "Myp4s.s3"},
        ).get("author")

        # tenta acessar as informacoes do another_user com o token do user
        response = self.get_author_response(
            token=user_token, id=another_user.id
        )
        self.assertAlmostEqual(response.status_code, 404)
