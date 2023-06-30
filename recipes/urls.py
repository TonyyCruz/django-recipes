from django.urls import include, path
from rest_framework.routers import SimpleRouter

from recipes import views

app_name = "recipes"

recipe_api_v2_router = SimpleRouter()
recipe_api_v2_router.register(
    prefix="recipes/api/v2",
    viewset=views.RecipeAPIv2ViewSet,
    basename="recipes-api",
)


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
        "recipes/tags/<slug:slug>/",
        views.RecipeViewTag.as_view(),
        name="tag",
    ),
    path(
        "recipes/api/v1/",
        views.RecipeViewHomeApiV1.as_view(),
        name="recipes_api_v1",
    ),
    path(
        "recipes/api/v1/<int:pk>/",
        views.RecipeViewDetailApiV1.as_view(),
        name="recipes_details_api_v1",
    ),
    path("", include(recipe_api_v2_router.urls)),
    path(
        "recipes/api/v2/tag/<int:pk>/",
        views.recipe_api_tag,
        name="recipes_tag_api_v2",
    ),
]
