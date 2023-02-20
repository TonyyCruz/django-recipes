from django.shortcuts import render


def recipes(request):
    return render(request, "calories_counter/pages/recipes.html")


def recipe(request, id):
    return render(request, "calories_counter/pages/recipe.html")
