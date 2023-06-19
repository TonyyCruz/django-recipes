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
        views.RecipeViewHomeApiV1.as_view(),
        name="recipes_api_v1",
    ),
    path(
        "recipes/api/v1/<int:pk>/",
        views.RecipeViewDetailApiV1.as_view(),
        name="details_api_v1",
    ),
    path(
        "theory/",
        views.theory,
        name="theory",
    ),
    path(
        "recipes/tags/<slug:slug>/",
        views.RecipeViewTag.as_view(),
        name="tag",
    ),
]
