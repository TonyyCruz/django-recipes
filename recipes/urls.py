from django.urls import path

from . import views

app_name = "recipes"


urlpatterns = [
    path("recipes/search/", views.search, name="search"),
    path("", views.home, name="home"),
    path("recipe/<int:id>/", views.recipe_details, name="details"),
    path("recipes/category/<int:id>/", views.category, name="category"),
]
