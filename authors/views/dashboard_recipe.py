from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from authors.forms.recipe_form import RecipeForm
from recipes.models import Recipe


class DashboardRecipe(View):
    def get_recipe(self, id, author):
        if id is None:
            return None

        recipe = Recipe.objects.filter(
            id=id,
            author=author,
            is_published=False,
        ).first()

        if not recipe:
            raise Http404()

        return recipe

    def render_recipe(self, form, page_title="Recipe edit"):
        return render(
            self.request,
            "authors/pages/dashboard_recipe.html",
            context={
                "page_title": page_title,
                "form": form,
            },
        )

    def get(self, request, id=None):
        recipe = self.get_recipe(id=id, author=request.user)
        form = RecipeForm(instance=recipe)

        return self.render_recipe(form=form)

    def post(self, request, id=None):
        recipe = self.get_recipe(id=id, author=request.user)
        form = RecipeForm(
            request.POST or None,
            files=request.FILES or None,
            instance=recipe,
        )

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False
            recipe.save()

            messages.success(request, "Recipe update successfully")
            return redirect(
                reverse(
                    "authors:dashboard_recipe_edit",
                    kwargs={"id": recipe.id},
                )
            )
        return self.render_recipe(form=form)
