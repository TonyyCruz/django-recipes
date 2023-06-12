from django.urls import path

from . import views

app_name = "recipes"


urlpatterns = [
    path("", views.RecipeViewHome.as_view(), name="home"),
    path("recipes/search/", views.RecipeViewSearch.as_view(), name="search"),
    path("recipe/<int:pk>/", views.RecipeViewDetail.as_view(), name="details"),
    path(
        "recipes/category/<int:id>/",
        views.RecipeViewCategory.as_view(),
        name="category",
    ),
    path(
        "recipes/api/v1/",
        views.RecipeViewHomeApi.as_view(),
        name="recipes_api",
    ),
]
