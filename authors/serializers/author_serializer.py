from django.contrib.auth import get_user_model
from rest_framework import serializers

from authors.validators import AuthorValidator


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        ]

        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        AuthorValidator(
            data=attrs,
            ErrorClass=serializers.ValidationError,
            partial_update=self.partial,
            fields=self.fields,
        )
        return super().validate(attrs)
