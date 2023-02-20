from django.urls import path

from . import views

urlpatterns = [
    path("", views.recipes),
    path("/recipe/<id>/", views.recipe),
]
