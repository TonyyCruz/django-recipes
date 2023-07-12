from django.urls import reverse

from .django_test_base import DjangoTestCaseWithSetup


# flake8:noqa
class AuthorDashboardIntegrationTest(DjangoTestCaseWithSetup):
    url_dashboard = reverse("authors:dashboard")
    url_dashboard_recipe_delete = reverse("authors:dashboard_recipe_create")

    def test_author_dashboard_is_not_accessible_by_unauthenticated_user(self):
        response = self.client.get(self.url_dashboard)
        self.assertEqual(response.status_code, 302)

    def test_author_dashboard_unauthenticated_user_is_redirect_to_login(self):
        response = self.client.get(self.url_dashboard, follow=True)

        content = response.content.decode("utf-8")

        self.assertIn("Login", content)
        self.assertNotIn("Dashboard", content)

    def test_author_dashboard_authenticated_user_can_access_dashboard(self):
        self.create_dummy_user()
        self.login_dummy_user()

        response = self.client.get(self.url_dashboard)

        content = response.content.decode("utf-8")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Dashboard", content)

    def test_author_dashboard_authenticated_user_can_create_a_recipe(self):
        self.create_dummy_user()
        self.login_dummy_user()

        response = self.client.post(
            self.url_dashboard_recipe_delete, data=self.mock_recipe_dict
        )

        content = response.content.decode("utf-8")

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.mock_recipe_dict["title"], content)

    def test_author_dashboard_authenticated_user_can_delete_a_recipe(self):
        # cria um author
        author = self.make_author(**self.mock_author_dict)
        # loga o author
        login = self.login_dummy_user(**self.mock_author_dict)
        # cria duas receitas nao publicadas com o author criado
        recipe_1, recipe_2 = self.make_multiples_recipes(
            author=author,
            quantity=2,
            is_published=False,
        )

        # deleta a "recipe_1"
        response = self.client.post(
            reverse(
                "authors:dashboard_recipe_delete", kwargs={"id": recipe_1.id}
            ),
            follow=True,
        )

        content = response.content.decode("utf-8")

        self.assertEqual(response.status_code, 200)
        # verifica se a recipe_1 nao esta na dashboard
        self.assertNotIn(recipe_1.title, content)
        # verifica se a recipe_2 esta na dashboard
        self.assertIn(recipe_2.title, content)
