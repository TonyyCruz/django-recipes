import os

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.generic import ListView

from utils.pagination import make_pagination

from .models import Category, Recipe

ITEMS_PER_PAGE = int(os.environ.get("ITEMS_PER_PAGE", 12))
QTY_PAGES_IN_PAGINATION = int(os.environ.get("QTY_PAGES_IN_PAGINATION", 5))


class RecipeListViewBase(ListView):
    model = Recipe
    paginate_by = None
    context_object_name = "recipes"
    ordering = ["-id"]

    def get_queryset(self, *args, **kwargs):
        current_queryset = super().get_queryset(*args, **kwargs)
        new_queryset = current_queryset.filter(
            is_published=True,
        )

        return new_queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        pages_obj, pagination_range = make_pagination(
            request=self.request,
            object_list=context.get("recipes"),
            per_page=ITEMS_PER_PAGE,
            qty_pages=QTY_PAGES_IN_PAGINATION,
        )

        context["is_recipe_list"] = True
        context["recipes"] = pages_obj
        context["pagination_range"] = pagination_range

        return context


class RecipeViewHome(RecipeListViewBase):
    template_name = "recipes/pages/home.html"


class RecipeViewCategory(RecipeListViewBase):
    template_name = "recipes/pages/category.html"

    def get_queryset(self, *args, **kwargs):
        current_queryset = super().get_queryset(*args, **kwargs)
        new_queryset = current_queryset.filter(category__id=self.kwargs["id"])

        return new_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def recipe_details(request, id):
    recipe = get_object_or_404(
        Recipe.objects.filter(
            id=id,
            is_published=True,
        )
    )
    return render(
        request,
        "recipes/pages/recipe_details.html",
        context={
            "recipe": recipe,
        },
    )


def category(request, id):
    category = get_object_or_404(Category, id=id)
    recipes = get_list_or_404(
        Recipe.objects.filter(is_published=True, category__id=id).order_by(
            "-id"
        )
    )
    pages_obj, pagination_range = make_pagination(
        request,
        recipes,
        ITEMS_PER_PAGE,
        qty_pages=QTY_PAGES_IN_PAGINATION,
    )

    return render(
        request,
        "recipes/pages/category.html",
        context={
            "pagination_range": pagination_range,
            "recipes": pages_obj,
            "is_recipe_list": True,
            "category": category,
        },
    )


def search(request):
    search_therm = request.GET.get("q", "").strip()
    recipes = Recipe.objects.filter(
        Q(title__icontains=search_therm)
        | Q(description__icontains=search_therm),
        is_published=True,
    ).order_by("-id")

    if not search_therm:
        raise Http404()

    pages_obj, pagination_range = make_pagination(
        request,
        recipes,
        ITEMS_PER_PAGE,
        qty_pages=QTY_PAGES_IN_PAGINATION,
    )

    return render(
        request,
        "recipes/pages/search.html",
        context={
            "pagination_range": pagination_range,
            "recipes": pages_obj,
            "page_title": f'Search: "{search_therm}"',
            "is_recipe_list": True,
            "additional_url_query": f"&q={search_therm}",
        },
    )
