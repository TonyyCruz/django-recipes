from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tag.models import Tag

from ..models import Recipe
from ..permissions import isOwner
from ..serializers import RecipeSerializer, TagSerializer


class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 12


class RecipeAPIv2ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "head", "options", "post", "patch", "delete"]

    def get_object(self):
        pk = self.kwargs.get("pk", "")
        obj = get_object_or_404(
            self.get_queryset(),
            pk=pk,
        )

        self.check_object_permissions(request=self.request, obj=obj)

        return obj

    def get_queryset(self):
        qs = super().get_queryset()
        category_id = self.request.query_params.get("category_id", "")

        if category_id != "" and category_id.isnumeric():
            qs.filter(category_id=category_id)
        return qs

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [isOwner()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        request.data["author"] = request.user.pk
        return super().create(request, *args, **kwargs)


@api_view()
def recipe_api_tag(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk,
    )
    serializer = TagSerializer(instance=tag, many=False)
    return Response(serializer.data)
