from django.urls import path

from . import views

app_name = "recipes"


urlpatterns = [
    path("", views.RecipeViewHome.as_view(), name="home"),
    path("recipes/search/", views.RecipeViewSearch.as_view(), name="search"),
    path("recipe/<int:id>/", views.recipe_details, name="details"),
    path(
        "recipes/category/<int:id>/",
        views.RecipeViewCategory.as_view(),
        name="category",
    ),
]
