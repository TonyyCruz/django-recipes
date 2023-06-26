from django.contrib.auth.models import User
from rest_framework import serializers

from tag.models import Tag

from .tag_serializer import TagSerializer


class RecipeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=65)
    description = serializers.CharField(max_length=165)
    # Utilizamos "source" para indicar o campo origem, caso os nomes dos campo
    # sejam diferentes
    public = serializers.BooleanField(source="is_published")
    preparation = serializers.SerializerMethodField()
    category = serializers.StringRelatedField()
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )
    tag = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    tag_objects = TagSerializer(
        many=True,
        source="tag",
    )
    tag_links = serializers.HyperlinkedRelatedField(
        source="tag",
        many=True,
        queryset=Tag.objects.all(),
        view_name="recipes:recipes_tag_api_v2",
    )

    # informa para "preparation" qual sera seu valor.
    # (atravez do SerializerMethodField), adicionamos get_<field>
    def get_preparation(self, recipe):
        return f"{recipe.preparation_time} {recipe.preparation_time_unit}"
