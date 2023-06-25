from rest_framework import serializers


class RecipeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=65)
    description = serializers.CharField(max_length=165)
    # Utilizamos "source" para indicar o campo origem, caso os nomes dos campo
    # sejam diferentes
    public = serializers.BooleanField(source="is_published")
    preparation = serializers.SerializerMethodField()

    # informa para "preparation" qual sera seu valor.
    # (atravez do SerializerMethodField), adicionamos get_<field>
    def get_preparation(self, recipe):
        return f"{recipe.preparation_time} {recipe.preparation_time_unit}"
