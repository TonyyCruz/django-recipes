from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Confirme sua senha",
        }),
        label="Confirmar senha"
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
            "password": forms.PasswordInput(attrs={
                "placeholder": "Insira sua senha aqui"
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            error_message = 'Os campos "senha" e "confirmar senha" precisam ser iguais'  # noqa: E501
            raise ValidationError({
                "password": error_message,
                "confirm_password": error_message,
            },
                code="invalid"
            )
