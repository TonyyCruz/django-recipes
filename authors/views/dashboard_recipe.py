from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.views import View

from authors.forms.recipe_form import RecipeForm
from recipes.models import Recipe


class DashboardRecipe(View):
    def get_recipe(self, id, author):
        recipe = Recipe.objects.filter(
            id=id,
            author=author,
            is_published=False,
        ).first()

        if not recipe:
            raise Http404()

        return recipe

    def render_recipe(self, form, page_title="page"):
        return render(
            self.request,
            "authors/pages/dashboard_recipe.html",
            context={
                "page_title": page_title,
                "form": form,
            },
        )

    @login_required(login_url="authors:login", redirect_field_name="next")
    def get(self, request, id):
        recipe = self.get_recipe(id=id, author=request.user)
        form = RecipeForm(instance=recipe)

        return self.render_recipe(
            form=form,
            page_title="Recipe edit",
        )

    @login_required(login_url="authors:login", redirect_field_name="next")
    def post(self, request, id):
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
            return self.render_recipe(
                form=form,
                page_title="Recipe edit",
            )
