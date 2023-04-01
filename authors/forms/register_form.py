from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils.django_form import strong_password


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        required=True,
        widget=forms.PasswordInput(attrs={
            "placeholder": "[a-z] [A-Z] [0-9] [@*!#$%?]",
        }),
        min_length=8,
        validators=[strong_password],
        help_text=(
            "Password must have at least 8 characters "
            "containing at least one uppercase, "
            "one lowercase one number and one special character."
        ),
        error_messages={
            "required": "Password must not be empty",
            "min_length": "Password must have at least 8 characters",
        },
    )

    confirm_password = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Repeat you password",
        }),
        min_length=8,
        error_messages={
            "required": "Confirm password must not be empty",
        },
    )

    username = forms.CharField(
        label='Username',
        required=True,
        help_text=(
            "Username must have letters, numbers or one of those @.+-_. "
            "The length should be between 4 and 150 characters."
        ),
        error_messages={
            "required": "Username must not be empty",
            "min_length": "Username must have at least 4 characters",
            "max_length": "Username must have less than 150 characters",
        },
        min_length=4,
        max_length=150,
        widget=forms.TextInput(attrs={
            "placeholder": "Ex.: @carol"
        }),
    )

    email = forms.EmailField(
        label="E-mail",
        required=True,
        widget=forms.EmailInput(
            attrs={"placeholder": "Ex.: email@email.com"}
        ),
        error_messages={
            "required": "E-mail must not be empty",
        }
    )

    first_name = forms.CharField(
        label="First name",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Ex.: Ana"}),
        min_length=2,
        error_messages={
            "required": "First name must not be empty",
            "min_length": "First name must have at least 2 characters",
        },
    )

    last_name = forms.CharField(
        label="Last name",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Ex.: Carolina"}),
        error_messages={
            "required": "Last name must not be empty",
        },
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

    def clean_email(self):
        email = self.cleaned_data.get("email", "")
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                "This email is already in use"
            )
        return email

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
