from django.urls import path

from calories_counter.views import home

urlpatterns = [
    path("", home)
]
