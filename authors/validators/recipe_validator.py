from collections import defaultdict

from django.core.exceptions import ValidationError

# from django.utils.text import slugify

# from recipes.models import Recipe


class RecipeValidator:
    def __init__(self, data, errors=None, ErrorClass=None, ignore_fields=None):
        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.data = data
        self.ignore_fields = (
            tuple() if ignore_fields is None else ignore_fields
        )
        self.clean()

    def methods_call_manager(self):
        my_validate_methods = [
            method_name
            for method_name in dir(RecipeValidator)
            if method_name.startswith("clean_")
        ]

        methods_to_call = [
            method_name
            for method_name in my_validate_methods
            if method_name[6:] not in self.ignore_fields
        ]

        for method in methods_to_call:
            method_select = getattr(self, method)
            method_select()

    def clean(self):
        self.methods_call_manager()

        if self.errors:
            raise self.ErrorClass(self.errors)

    def clean_title(self):
        title = self.data.get("title", "")

        if not title:
            self.errors["title"].append("Title must not be empty")

        if len(title) < 5:
            self.errors["title"].append("Title must have at least 5 chars")

        if len(title) > 150:
            self.errors["title"].append(
                "Title must have less than 150 characters"
            )

        # title_slug = slugify(title)
        # slug_title_exists = Recipe.objects.filter(slug=title_slug).exists()

        # if slug_title_exists:
        #     self.errors["title"].append("This recipe title already exists")

        return title

    def clean_description(self):
        title = self.data.get("title", "")
        description = self.data.get("description", "")

        if not description:
            self.errors["description"].append("Description must not be empty")

        if len(description) < 5:
            self.errors["description"].append(
                "Description must have at least 5 chars"
            )

        if title == description:
            self.errors["description"].append(
                "Description cannot be equal to title"
            )

        return description

    def clean_preparation_time(self):
        preparation_time = self.data.get("preparation_time", "")

        if not isinstance(preparation_time, int) or preparation_time <= 0:
            self.errors["preparation_time"].append(
                "Preparation time must be an integer greater than 0"
            )

        return preparation_time

    def clean_preparation_time_unit(self):
        preparation_time_unit = self.data.get("preparation_time_unit", "")

        if not preparation_time_unit:
            self.errors["preparation_time_unit"].append(
                "Preparation time unit is required"
            )

        return preparation_time_unit

    def clean_servings(self):
        servings = self.data.get("servings", "")

        if not isinstance(servings, int) or servings <= 0:
            self.errors["servings"].append(
                "Servings time must be an integer greater than 0"
            )

        return servings

    def clean_servings_unit(self):
        servings_unit = self.data.get("servings_unit", "")

        if not servings_unit:
            self.errors["servings_unit"].append("Serving unit is required")

        return servings_unit

    def clean_preparation_steps(self):
        preparation_steps = self.data.get("preparation_steps", "")
        if len(preparation_steps) < 50:
            self.errors["preparation_steps"].append(
                "Preparation steps must have at least 50 characters"
            )
