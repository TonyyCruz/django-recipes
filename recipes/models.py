from collections import defaultdict

from django.contrib.auth.models import User
from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.forms import ValidationError
from django.urls import reverse
from django.utils.text import slugify

from tag.models import Tag
from utils.image_helper import resize_image


class Category(models.Model):
    name = models.CharField(max_length=65)

    def get_absolute_url(self):
        return reverse("recipes:category", kwargs={"id": self.id})

    def __str__(self):
        return self.name


class RecipeManager(models.Manager):
    def get_published(self):
        return (
            self.filter(is_published=True)
            .annotate(
                author_full_name=Concat(
                    F("author__first_name"),
                    Value(" "),
                    F("author__last_name"),
                    Value(" ("),
                    F("author__username"),
                    Value(")"),
                )
            )
            .order_by("-id")
            .select_related("category", "author")
            .prefetch_related("tags")
        )


class Recipe(models.Model):
    objects = RecipeManager()
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to="recipes/covers/%Y/%m/%d",
        editable=True,
        default="base_images/recipes/covers/No-Image-Placeholder.svg.png",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_DEFAULT,
        default=1,
    )
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    tag = models.ManyToManyField(Tag, blank=True, default="None")

    def get_absolute_url(self):
        return reverse("recipes:details", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f"{slugify(self.title)}"
            self.slug = slug

        saved = super().save(*args, **kwargs)

        if self.cover:
            try:
                resize_image(self.cover, 840)
            except FileNotFoundError:
                ...

        return saved

    def __str__(self):
        return self.title

    # Validacao de campos feito no models (o mesmo que foi feito no forms)
    def clean(self, *args, **kwargs):
        error_messages = defaultdict(list)

        recipe_from_db = Recipe.objects.filter(
            title__iexact=self.title
        ).first()

        if recipe_from_db:
            if recipe_from_db.pk != self.pk:
                error_messages["title"].append(
                    "Found recipes with the same title"
                )

        if error_messages:
            raise ValidationError(error_messages)
