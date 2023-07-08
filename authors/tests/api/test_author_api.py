from rest_framework import test

from recipes.tests.recipe_test_base import RecipeMixing


class AuthorsAPIv2Test(test.APITestCase, RecipeMixing):
    def test_test(self):
        assert 1 > 0
