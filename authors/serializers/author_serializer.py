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
        data = dict(attrs)
        confirm_password = self.initial_data.get("confirm_password", "")
        if confirm_password:
            data["confirm_password"] = confirm_password

        AuthorValidator(
            data=data,
            ErrorClass=serializers.ValidationError,
            partial_update=self.partial,
            fields=self.fields,
        )
        return super().validate(attrs)

    def create(self, validated_data):
        return super().create(validated_data)
