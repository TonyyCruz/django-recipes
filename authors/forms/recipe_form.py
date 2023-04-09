from django import forms

from recipes.models import Recipe


class RecipeForm(forms.ModelForm):
    preparation_steps = forms.FileField(
        label="Preparation steps",
        required=True,
        widget=forms.Textarea(attrs={
            "placeholder": "Write the preparation steps",
            "class": "span-2"
        })
    )

    cover = forms.ImageField(
        label="Cover",
        required=True,
        widget=forms.FileInput(attrs={
            "class": "span-2"
        })
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
            "preparation_steps",
            "cover",
            "category",
            "preparation_steps_is_html",
        ]
