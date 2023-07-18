from .base_validate import BaseValidator

# from django.utils.text import slugify

# from recipes.models import Recipe


class RecipeValidator(BaseValidator):
    def validate_title(self):
        title = self.data.get("title", "")

        if not title:
            self.errors["title"].append("Title must not be empty.")

        if len(title) < 5:
            self.errors["title"].append("Title must have at least 5 chars.")

        if len(title) > 65:
            self.errors["title"].append(
                "Title must have less than 65 characters."
            )

        # title_slug = slugify(title)
        # slug_title_exists = Recipe.objects.filter(slug=title_slug).exists()

        # if slug_title_exists:
        #     self.errors["title"].append("This recipe title already exists")

    def validate_description(self):
        description = self.data.get("description", "")
        title = self.data.get("title", "")

        if not description:
            self.errors["description"].append("Description must not be empty.")

        if len(description) < 5:
            self.errors["description"].append(
                "Description must have at least 5 chars."
            )

        if len(description) > 165:
            self.errors["title"].append(
                "Description must have less than 165 characters."
            )

        if title == description:
            self.errors["description"].append(
                "Description cannot be equal to title."
            )

    def validate_preparation_time(self):
        preparation_time = self.data.get("preparation_time", "")

        if not isinstance(preparation_time, int) or preparation_time <= 0:
            self.errors["preparation_time"].append(
                "Preparation time must be an integer greater than 0."
            )

    def validate_preparation_time_unit(self):
        preparation_time_unit = self.data.get("preparation_time_unit", "")

        if not preparation_time_unit:
            self.errors["preparation_time_unit"].append(
                "Preparation time unit is required."
            )

        if preparation_time_unit not in ("minute", "hour"):
            self.errors["preparation_time_unit"].append(
                'Preparation time unit must be "minute" or "hour".'
            )

    def validate_servings(self):
        servings = self.data.get("servings", "")

        if not isinstance(servings, int) or servings <= 0:
            self.errors["servings"].append(
                "Servings time must be an integer greater than 0."
            )

    def validate_servings_unit(self):
        servings_unit = self.data.get("servings_unit", "")

        if not servings_unit:
            self.errors["servings_unit"].append("Serving unit is required.")

        if servings_unit not in ("portion", "unit", "piece"):
            self.errors["servings_unit"].append(
                'Serving unit must be "portion", "unit" or "piece".'
            )

    def validate_preparation_steps(self):
        preparation_steps = self.data.get("preparation_steps", "")
        if len(preparation_steps) < 50:
            self.errors["preparation_steps"].append(
                "Preparation steps must have at least 50 characters."
            )
