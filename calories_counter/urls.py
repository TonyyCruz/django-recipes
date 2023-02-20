from django.urls import path

from . import views

urlpatterns = [
    path("recipes", views.recipe_list),
    path("recipe/<int:id>/", views.recipe),
]
