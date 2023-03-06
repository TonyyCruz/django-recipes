from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
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
