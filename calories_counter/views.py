from django.shortcuts import get_list_or_404, get_object_or_404, render

from .models import Category, Recipe


def home(request):
    return render(request, "calories_counter/pages/home.html")


def recipe_list(request):
    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by("-id")

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
    category = get_object_or_404(Category, id=id)
    recipes = get_list_or_404(
        Recipe.objects.filter(
            is_published=True,
            category__id=id
        ).order_by("-id")
    )

    return render(
        request,
        "calories_counter/pages/category.html",
        context={
            "recipes": recipes,
            "category": category,
            "is_recipe_list": True,
        })
