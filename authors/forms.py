import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def strong_password(password):
    regex = re.compile(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$"
    )
    if not regex.match(password):
        raise ValidationError((
            """
            Password must have at least one uppercase letter,
            one lowercase letter and one number. The length should be
            at least 8 characters.
            """
        ),
            code="Invalid"
        )


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "[a-z] [A-Z] [@*!#$%.?]",
        }),
        validators=[strong_password],
        help_text=(
            """
            Requires 8 characters containing at least
            one uppercase, one lowercase and one special character
            """
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Repeat you password",
        }),
        label="Confirm password",
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password"
        ]
        labels = {
            "username": "User",
            "first_name": "Name",
            "last_name": "Last name",
            "email": "E-mail",
            "password": "Password",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={
                "placeholder": "Ex:.Ana"
            }),
            "last_name": forms.TextInput(attrs={
                "placeholder": "Ex:.Carolina"
            }),
            "username": forms.TextInput(attrs={
                "placeholder": "Ex:.@carol"
            }),
            "email": forms.TextInput(attrs={
                "placeholder": "Ex:.email@email.com"
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            error_message = '"Password" and "Confirm password" must be equal'
            raise ValidationError({
                "confirm_password": error_message,
            },
                code="Invalid"
            )
