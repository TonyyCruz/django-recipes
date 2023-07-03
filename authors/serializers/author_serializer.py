from django.contrib.auth.models import User
from rest_framework import serializers

from authors.validators import AuthorValidator


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        ]

    def validate(self, attrs):
        AuthorValidator(
            data=attrs,
            ErrorClass=serializers.ValidationError,
            partial_update=self.partial,
            fields=self.fields,
        )
        return super().validate(attrs)
