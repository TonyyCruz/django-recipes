from django.contrib.auth.models import User
from django.test import TestCase

from recipes.models import Category, Recipe


class TestCaseWithSetup(TestCase):
    # def setUp(self):
    #     self.make_recipe()
    #     return super().setUp()

    def make_category(self, name="category"):
        return Category.objects.create(name=name)

    def make_author(
        self,
        first_name="user",
        last_name="name",
        username="user_name",
        password="123456",
        email="user@user.com",
    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_recipe(
        self,
        category=None,
        author=None,
        title="My test title",
        description="description",
        slug="slug",
        preparation_time=10,
        preparation_time_unit="minutos",
        servings=3,
        servings_unit="porcoes",
        preparation_steps="cozinha e come",
        preparation_steps_is_html=False,
        is_published=True,
    ):
        if category is None:
            category = self.make_category()
        if author is None:
            author = self.make_author()

        return Recipe.objects.create(
            category=category,
            author=author,
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
        )
