import os

# o "F" é usado para informar que a string é um campo do model
from django.db.models import F, Q, Value
from django.db.models.aggregates import Count
from django.db.models.functions import Concat
from django.forms.models import model_to_dict
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from utils.pagination import make_pagination

from .models import Recipe

ITEMS_PER_PAGE = int(os.environ.get("ITEMS_PER_PAGE", 12))
QTY_PAGES_IN_PAGINATION = int(os.environ.get("QTY_PAGES_IN_PAGINATION", 5))


def theory(request, *args, **kwargs):
    recipes = Recipe.objects.all()[:10]

    # Contando as reeceitas
    number_of_recipes = recipes.aggregate(Count("id"))
    # number_of_recipes = Recipe.objects.aggregate(Count("id"))

    # São mais rapidas
    simple_recipes = Recipe.objects.values(
        "id", "title", "author__first_name"
    ).filter(title__icontains="frango")[:10]

    # Criar novo campo na resposta da query
    novo_campo = Recipe.objects.all().annotate(
        author_full_name=Concat(
            F("author__first_name"),
            Value(" "),  # O value foi usado para adicionar um espaço vazio
            F("author__last_name"),
        )
    )[:5]

    context = {
        "recipes": recipes,
        "simple_recipes": simple_recipes,
        "number_of_recipes": number_of_recipes["id__count"],
        "novo_campo": novo_campo,
    }
    return render(request, "recipes/pages/theory.html", context=context)


class RecipeListViewBase(ListView):
    model = Recipe
    paginate_by = None
    context_object_name = "recipes"
    ordering = ["-id"]

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )

        qs = qs.select_related("author", "category")

        return qs

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


class RecipeViewHomeApiV1(RecipeListViewBase):
    template_name = "recipes/pages/home.html"

    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data()["recipes"]
        recipes_list = recipes.object_list.values()
        return JsonResponse(
            list(recipes_list),
            safe=False,
        )


class RecipeViewCategory(RecipeListViewBase):
    template_name = "recipes/pages/category.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(category__id=self.kwargs.get("id"))

        if not qs:
            raise Http404()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_name = context.get("recipes")[0].category.name
        context["page_title"] = f"Category {category_name}"
        return context


class RecipeViewSearch(RecipeListViewBase):
    template_name = "recipes/pages/search.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        search_therm = self.request.GET.get("q", "").strip()

        if not search_therm:
            raise Http404()

        qs = qs.filter(
            Q(title__icontains=search_therm)
            | Q(description__icontains=search_therm),
            is_published=True,
        )

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_therm = self.request.GET.get("q", "").strip()
        context["search_therm"] = f"{search_therm}"
        context["additional_url_query"] = f"&q={search_therm}"
        return context


class RecipeViewDetail(DetailView):
    model = Recipe
    context_object_name = "recipe"
    template_name = "recipes/pages/recipe_details.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)

        return qs


class RecipeViewDetailApiV1(RecipeViewDetail):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data(context, **response_kwargs)["recipe"]
        recipe_dict = model_to_dict(recipe)

        recipe_dict["created_at"] = str(recipe.created_at)
        recipe_dict["updated_at"] = str(recipe.updated_at)

        if recipe_dict.get("cover"):
            recipe_dict["cover"] = (
                self.request.build_absolute_uri()[:-21]
                + recipe_dict["cover"].url
            )
        else:
            recipe_dict["cover"] = ""

        del recipe_dict["is_published"]

        return JsonResponse(
            recipe_dict,
            safe=False,
        )
