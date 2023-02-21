from django.shortcuts import render

from calories_counter.utils.calories_counter.factory import make_recipe


def recipe_list(request):
    return render(
        request,
        "calories_counter/pages/recipe_list.html",
        context={
            "recipes": [make_recipe() for _ in range(10)],
            "is_recipe_list": True,
        })


def recipe_details(request, id):
    return render(
        request,
        "calories_counter/pages/recipe_detail.html",
        context={
            "recipe": make_recipe(),
        })
