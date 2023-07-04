from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from authors.validators import AuthorValidator

# from utils.django_form import strong_password


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "[a-z] [A-Z] [0-9] [@*!#$%?]",
            }
        ),
        help_text=(
            "Password must have at least 8 characters "
            "containing at least one uppercase, "
            "one lowercase one number and one special character."
        ),
    )

    confirm_password = forms.CharField(
        label="Confirm password",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Repeat you password",
            }
        ),
    )

    username = forms.CharField(
        label="Username",
        required=True,
        help_text=("The length should be between 4 and 150 characters."),
        widget=forms.TextInput(attrs={"placeholder": "Ex.: @carol"}),
    )

    email = forms.EmailField(
        label="E-mail",
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Ex.: email@email.com"}),
    )

    first_name = forms.CharField(
        label="First name",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Ex.: Ana"}),
    )

    last_name = forms.CharField(
        label="Last name",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Ex.: Carolina"}),
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "confirm_password",
        ]

    def clean(self):
        AuthorValidator(data=self.cleaned_data, ErrorClass=ValidationError)

        return super().clean()
