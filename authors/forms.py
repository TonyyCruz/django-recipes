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
            "Senha precisa ter pelo menos 8 caracteres, "
            "precisa ter pelo menos um caractere maiúsculo, "
            "um maiúsculo e um caractere especial"
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
            """Requer 8 charactres contendo no mínimo
            um maiúsculo, um minúsculo e um especial"""
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Repita sua senha",
        }),
        label="Confirmar senha",
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
            "username": "Usuário",
            "first_name": "Nome",
            "last_name": "Sobrenome",
            "email": "E-mail",
            "password": "Senha",
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
                "placeholder": "Ex:. seuEmail@email.com"
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            error_message = 'Os campos "senha" e "confirmar senha" precisam ser iguais'  # noqa: E501
            raise ValidationError({
                "confirm_password": error_message,
            },
                code="Invalid"
            )
