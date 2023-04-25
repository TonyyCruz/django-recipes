from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views

from .recipe_test_base import RecipeTestBase


class RecipesCategoryViews(RecipeTestBase):
    def test_recipe_category_uses_correct_view(self):
        view = resolve(reverse("recipes:category", kwargs={"id": 1}))
        self.assertIs(views.RecipeViewCategory, view.func.view_class)

    def test_recipe_category_view_return_status_404_if_category_no_exists(
        self,
    ):
        response = self.client.get(
            reverse("recipes:category", kwargs={"id": 999})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_return_status_404_if_recipe_not_published(self):
        # category raises 404 if there are no published recipes
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse("recipes:category", kwargs={"id": recipe.category.id})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_have_a_correct_pagination_range(self):
        category = self.make_category(name="test_category")
        self.make_multiples_recipes(quantity=18, category=category)

        with patch("recipes.views.ITEMS_PER_PAGE", new=3):
            response = self.client.get(
                reverse("recipes:category", kwargs={"id": category.id})
                + "?page=1"
            )
            response_2 = self.client.get(
                reverse("recipes:category", kwargs={"id": category.id})
                + "?page=3"
            )
            response_3 = self.client.get(
                reverse("recipes:category", kwargs={"id": category.id})
                + "?page=4"
            )

            context = response.context["pagination_range"]
            context_2 = response_2.context["pagination_range"]
            context_3 = response_3.context["pagination_range"]

            content = response.content.decode("utf-8")
            content_2 = response_2.content.decode("utf-8")
            content_3 = response_3.content.decode("utf-8")

            self.assertEqual(context["page_range"], range(1, 7))
            self.assertEqual(context["current_page"], 1)
            self.assertEqual(context["stop_range"], 5)
            self.assertIn('area-label="Current page 1"', content)

            self.assertEqual(context_2["page_range"], range(1, 7))
            self.assertEqual(context_2["current_page"], 3)
            self.assertEqual(context_2["stop_range"], 5)
            self.assertIn('area-label="Current page 3"', content_2)

            self.assertEqual(context_3["page_range"], range(1, 7))
            self.assertEqual(context_3["current_page"], 4)
            self.assertEqual(context_3["stop_range"], 6)
            self.assertIn('area-label="Current page 4"', content_3)

    def test_recipe_category_items_per_page_is_correct(self):
        category = self.make_category(name="test_category")
        self.make_multiples_recipes(quantity=10, category=category)
        with patch("recipes.views.ITEMS_PER_PAGE", new=3):
            response = self.client.get(
                reverse("recipes:category", kwargs={"id": category.id})
            )
            recipes = response.context["recipes"]
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 4)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 3)
            self.assertEqual(len(paginator.get_page(4)), 1)

    # def test_home_have_a_correct_page_title(self):
    #     category_name = "test_category"
    #     category = self.make_category(name=category_name)
    #     self.make_recipe(category=category)
    #     response = self.client.get(
    #         reverse("recipes:category", kwargs={"id": category.id})
    #     )
    #     content = response.content
    #     self.assertIn(
    #         f"<title>{category_name}</title>", content.decode("utf-8")
    #     )
