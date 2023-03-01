from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from .models import Category, Recipe


def home(request):
    return render(request, "recipes/pages/home.html")


def recipe_list(request):
    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by("-id")

    current_page = request.GET.get("page", 1)
    paginator = Paginator(recipes, 12)
    pages_obj = paginator.get_page(current_page)

    return render(
        request,
        "recipes/pages/recipe_list.html",
        context={
            "recipes": pages_obj,
            "is_recipe_list": True,
            "page_title": "Receitas",
        })


def recipe_details(request, id):
    recipe = get_object_or_404(
        Recipe.objects.filter(
            id=id,
            is_published=True,
        ))
    return render(
        request,
        "recipes/pages/recipe_details.html",
        context={
            "recipe": recipe,
            "page_title": recipe.title,
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
        "recipes/pages/category.html",
        context={
            "recipes": recipes,
            "is_recipe_list": True,
            "page_title": category.name,
        })


def search(request):
    search_therm = request.GET.get("q", "").strip()
    recipes = Recipe.objects.filter(
        Q(title__icontains=search_therm)
        | Q(description__icontains=search_therm),
        is_published=True,
    ).order_by("-id")

    if not search_therm:
        raise Http404()

    return render(
        request,
        "recipes/pages/search.html",
        context={
            "recipes": recipes,
            "page_title": f"Search: \"{search_therm}\"",
            "is_recipe_list": True,
        }
    )
