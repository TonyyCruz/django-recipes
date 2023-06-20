from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from tag.models import Tag


class Category(models.Model):
    name = models.CharField(max_length=65)

    def get_absolute_url(self):
        return reverse("recipes:category", kwargs={"id": self.id})

    def __str__(self):
        return self.name


class Recipe(models.Model):
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

    # Faz a relação com o Model genérico "Tag"
    tag = GenericRelation(Tag, related_query_name="recipes")

    def get_absolute_url(self):
        return reverse("recipes:details", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f"{slugify(self.title)}"
            self.slug = slug
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title
