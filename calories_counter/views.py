from django.shortcuts import render

from .models import Recipe

# from calories_counter.utils.calories_counter.factory import make_recipe


def home(request):
    return render(request, "calories_counter/pages/home.html")


def recipe_list(request):
    recipes = Recipe.objects.all().order_by("-id")
    return render(
        request,
        "calories_counter/pages/recipe_list.html",
        context={
            "recipes": recipes,
            "is_recipe_list": True,
        })


def recipe_details(request, id):
    recipe = Recipe.objects.get(id=id)
    return render(
        request,
        "calories_counter/pages/recipe_details.html",
        context={
            "recipe": recipe,
        })


def category(request, id):
    recipes = Recipe.objects.filter(
        category__id=id
    ).order_by("-id")
    return render(
        request,
        "calories_counter/pages/category.html",
        context={
            "recipes": recipes,
        })
