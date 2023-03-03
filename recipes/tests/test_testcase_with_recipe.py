from django.contrib.auth.models import User
from django.test import TestCase
from faker import Faker

from recipes.models import Category, Recipe

fake = Faker()


class TestCaseWithRecipe(TestCase):
    # def setUp(self):
    #     self.make_recipe()
    #     return super().setUp()

    def make_category(self, name="category"):
        return Category.objects.create(name=name)

    def make_author(
        self,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        username=None,
        password="123456",
        email=fake.email(),
    ):
        if username is None:
            username = first_name + last_name
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
        slug=fake.pystr_format(),
        preparation_time=10,
        preparation_time_unit="minutos",
        servings=3,
        servings_unit="porcoes",
        preparation_steps="cozinha e come",
        preparation_steps_is_html=False,
        is_published=True,
    ):
        params = {
            "category": category,
            "author": author,
            "title": title,
            "description": description,
            "slug": slug,
            "preparation_time": preparation_time,
            "preparation_time_unit": preparation_time_unit,
            "servings": servings,
            "servings_unit": servings_unit,
            "preparation_steps": preparation_steps,
            "preparation_steps_is_html": preparation_steps_is_html,
            "is_published": is_published,
        }
        if category is None:
            params["category"] = self.make_category()
        if author is None:
            params["author"] = self.make_author()
        if preparation_steps_is_html is None:
            params.pop("preparation_steps_is_html")
        if is_published is None:
            params.pop("is_published")

        return Recipe.objects.create(
            **params
        )

    def make_multiples_recipes(self, quantity=2):
        if quantity <= 0:
            raise ValueError("Quantity need be greater than 0")
        recipes = []
        for i in range(quantity):
            author = self.make_author(
                username=f"fake.name(){i}",
                email=f"fake.email(){i}"
            )

            recipes.append(self.make_recipe(author=author, slug=i))
        return recipes
