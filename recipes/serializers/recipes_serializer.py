from rest_framework import serializers

from authors.validators import RecipeValidator

from ..models import Recipe
from .tag_serializer import TagSerializer


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "description",
            "public",
            "preparation",
            "category",
            "author",
            "tag",
            "tag_objects",
            "tag_links",
            "preparation_time",
            "preparation_time_unit",
            "servings",
            "servings_unit",
            "preparation_steps",
            "cover",
        ]

    # Utilizamos "source" para indicar o campo origem, caso os nomes dos campo
    # sejam diferentes
    public = serializers.BooleanField(
        source="is_published",
        read_only=True,
    )
    # SerializerMethodField informa que o valor sera adquirido de um methodo
    preparation = serializers.SerializerMethodField(
        read_only=True,
    )
    # StringRelatedField exibe o valor do campo no lugar do "id"
    category = serializers.StringRelatedField(
        read_only=True,
    )
    tag_objects = TagSerializer(
        many=True,
        source="tag",
        read_only=True,
    )
    # HyperlinkedRelatedField serve para inserir um link no campo
    tag_links = serializers.HyperlinkedRelatedField(
        source="tag",
        many=True,
        view_name="recipes:recipes_tag_api_v2",
        read_only=True,
    )

    # informa para "preparation" qual sera seu valor.
    # (atravez do SerializerMethodField), adicionamos get_<field>
    def get_preparation(self, recipe):
        return f"{recipe.preparation_time} {recipe.preparation_time_unit}"

    # VALIDATIONS
    def validate(self, attrs):
        RecipeValidator(
            data=attrs,
            ErrorClass=serializers.ValidationError,
            partial_update=self.partial,
            fields=self.fields,
        )
        return super().validate(attrs)
