from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from tag.models import Tag

from ..models import Recipe
from ..serializers import RecipeSerializer, TagSerializer


class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 12


class RecipeAPIv2List(ListCreateAPIView):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination


class RecipeAPIv2Details(APIView):
    def get_recipe(self, pk):
        return get_object_or_404(
            Recipe.objects.get_published(),
            pk=pk,
        )

    def get(self, request, pk):
        recipe = self.get_recipe(pk)
        serializer = RecipeSerializer(
            instance=recipe,
            many=False,
            context={
                "request": request,
            },
        )
        return Response(serializer.data)

    def patch(self, request, pk):
        recipe = self.get_recipe(pk)
        serializer = RecipeSerializer(
            instance=recipe,
            many=False,
            data=request.data,
            partial=True,
            context={
                "request": request,
            },
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        recipe = self.get_recipe(pk)
        recipe.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=["get", "patch", "delete"])
def recipe_api_details(request, pk):
    recipe = get_object_or_404(
        Recipe.objects.get_published(),
        pk=pk,
    )
    if request.method == "GET":
        serializer = RecipeSerializer(
            instance=recipe,
            many=False,
            context={
                "request": request,
            },
        )
        return Response(serializer.data)

    elif request.method == "PATCH":
        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            many=False,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
        )

    elif request.method == "DELETE":
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def recipe_api_tag(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk,
    )
    serializer = TagSerializer(instance=tag, many=False)
    return Response(serializer.data)
