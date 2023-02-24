from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("recipes", views.recipe_list, name="recipe-list"),
    path("recipe/<int:id>/", views.recipe_details, name="recipe-details"),
    path("recipe/category/<int:id>/", views.category, name="recipe-category"),
]
