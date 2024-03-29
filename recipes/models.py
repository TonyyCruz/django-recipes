import string
from collections import defaultdict
from random import SystemRandom

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
    def get_published(self, pk=False):
        if pk:
            return (
                self.filter(is_published=True, pk=pk)
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
                .first()
            )

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
            .prefetch_related("tag")
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
        blank=True,
        editable=True,
        default="",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    tag = models.ManyToManyField(Tag, blank=True, default="")

    def get_absolute_url(self):
        return reverse("recipes:details", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        rand_letters = "".join(
            SystemRandom().choices(
                string.ascii_letters + string.digits,
                k=5,
            )
        )
        if not self.slug:
            slug = slugify(f"{self.title}-{rand_letters}")
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
                    "This recipe title already exists"
                )

        if error_messages:
            raise ValidationError(error_messages)
