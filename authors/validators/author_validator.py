from django.contrib.auth.models import User

from utils.django_form import strong_password

from .base_validate import BaseValidator


class AuthorValidator(BaseValidator):
    def validate_first_name(self):
        first_name = self.data.get("first_name", "")

        if not first_name:
            self.errors["first_name"].append("First name must not be empty")

        if len(first_name) < 2:
            self.errors["first_name"].append(
                "First name must have at least 2 characters"
            )

    def validate_last_name(self):
        last_name = self.data.get("last_name", "")

        if not last_name:
            self.errors["last_name"].append("Last name must not be empty")

    def validate_username(self):
        username = self.data.get("username", "")

        if not username:
            self.errors["username"].append("Username must not be empty")

        if len(username) < 4:
            self.errors["username"].append(
                "Username must have at least 4 characters"
            )

        if len(username) > 150:
            self.errors["username"].append(
                "Username must have less than 150 characters"
            )

        exists = User.objects.filter(username=username).exists()

        if exists:
            self.errors["username"].append("This username is already in use")

    def validate_email(self):
        email = self.data.get("email", "")

        if not email:
            self.errors["email"].append("E-mail must not be empty")

        exists = User.objects.filter(email=email).exists()

        if exists:
            self.errors["email"].append("This email is already in use")

    def validate_password(self):
        password = self.data.get("password", "")

        # if not password:
        #     self.errors["password"].append("Password must not be empty")

        # if len(password) < 8:
        #     self.errors["password"].append(
        #         "Password must have at least 8 characters"
        #     )

        is_the_password_weak = strong_password(password)
        if is_the_password_weak:
            self.errors["password"].append(is_the_password_weak)

    def validate_confirm_password(self):
        confirm_password = self.data.get("confirm_password", "")

        if not confirm_password:
            self.errors["confirm_password"].append(
                "Confirm password must not be empty"
            )

        password = self.data.get("password", "")

        if password != confirm_password:
            self.errors["confirm_password"].append(
                '"Password" and "Confirm password" must be equal'
            )
