from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from tag.models import Tag

from .models import Category, Recipe


class CategoryAdmin(admin.ModelAdmin):
    pass


# Seleciona o Model generico
class TagGeneric(GenericTabularInline):
    model = Tag
    fields = ["name"]
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "created_at", "author", "is_published"]
    list_display_links = ["title", "created_at"]
    search_fields = ["id", "title", "slug", "description", "preparation_steps"]
    list_filter = [
        "category",
        "author",
        "is_published",
        "preparation_steps_is_html",
    ]
    list_per_page = 15
    list_editable = ["is_published"]
    ordering = ["-id"]
    prepopulated_fields = {"slug": ["title"]}

    # Adiciona o campo genérico para manimpulação na tela de admin do django
    inlines = [
        TagGeneric,
    ]


admin.site.register(Category, CategoryAdmin)
