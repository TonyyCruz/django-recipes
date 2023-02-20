from django.shortcuts import render


def recipe_list(request):
    return render(request, "calories_counter/pages/recipe_list.html")


def recipe_details(request, id):
    return render(request, "calories_counter/pages/recipe_detail.html")
