from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from recipes.models import Recipe


class RecipeForm(forms.ModelForm):
    title = forms.CharField(
        label="Title",
        required=True,
        min_length=2,
        max_length=150,
        widget=forms.TextInput(
            attrs={"placeholder": "Write the recipe title here."},
        ),
        error_messages={
            "required": "Title must not be empty",
            "min_length": "Title must have at least 2 characters",
            "max_length": "Title must have less than 150 characters",
        },
    )

    preparation_steps = forms.CharField(
        label="Preparation steps",
        required=True,
        min_length=50,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Write the preparation steps",
                "class": "span-2",
            }
        ),
        error_messages={
            "required": "Preparation steps must not be empty",
            "min_length": "Preparation steps must have at least 50 characters",
        },
    )

    cover = forms.ImageField(
        label="Cover",
        required=True,
        widget=forms.FileInput(
            attrs={
                "class": "span-2",
            }
        ),
    )

    servings_unit = forms.CharField(
        required=True,
        widget=forms.Select(
            choices=[
                ("potions", "potions"),
                ("units", "units"),
                ("pieces", "pieces"),
            ],
        ),
    )

    preparation_time_unit = forms.CharField(
        widget=forms.Select(
            choices=[
                ("minute", "minute(s)"),
                ("hour", "hour(s)"),
            ],
        ),
    )

    class Meta:
        model = Recipe
        fields = [
            "title",
            "description",
            "preparation_time",
            "preparation_time_unit",
            "servings",
            "servings_unit",
            "category",
            "preparation_steps",
            # "preparation_steps_is_html",
            "cover",
        ]

        widgets = {
            "preparation_steps_is_html": forms.CheckboxInput(
                attrs={
                    "class": "checkbox",
                }
            ),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title", "")
        title_slug = slugify(title)
        slug_title_exists = Recipe.objects.filter(slug=title_slug).exists()

        if slug_title_exists:
            raise ValidationError("This recipe title already exists")

        return title
