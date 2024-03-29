from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError

from authors.validators import RecipeValidator
from recipes.models import Recipe


class RecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(list)

    title = forms.CharField(
        label="Title",
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Write the recipe title here."},
        ),
    )

    description = forms.CharField(
        label="Description",
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Write the recipe description here."},
        ),
    )

    preparation_steps = forms.CharField(
        label="Preparation steps",
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Write the preparation steps",
                "class": "span-2",
            }
        ),
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
        required=False,
        widget=forms.Select(
            choices=[
                ("portion", "portion"),
                ("unit", "unit"),
                ("piece", "piece"),
            ],
        ),
    )

    preparation_time_unit = forms.CharField(
        widget=forms.Select(
            choices=[
                ("minute", "minute"),
                ("hour", "hour"),
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
            "cover",
        ]

        widgets = {
            "preparation_steps_is_html": forms.CheckboxInput(
                attrs={
                    "class": "checkbox",
                }
            ),
        }

    def clean(self):
        RecipeValidator(data=self.cleaned_data, ErrorClass=ValidationError)

        return super().clean()
